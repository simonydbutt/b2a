from Backtest.main.Utils.MongoUtil import MongoUtil
from Backtest.main.Utils.TimeUtil import TimeUtil
import pandas as pd
import json
import requests
import time

class BinanceDS:

    """
        Datasource for Binance exchange
    """

    def __init__(self):
        self.MU = MongoUtil(dbName='binance')
        self.TU = TimeUtil()
        self.baseUrl = 'https://api.binance.com'
        self.bin2Time = {
            '1m': 60, '3m': 3*60, '5m': 5*60, '15m': 15*60,
            '30m': 30*60, '1h': 60*60, '2h': 2*60*60,
            '4h': 4*60*60, '6h': 6*60*60, '8h': 8*60*60,
            '12h': 12*60*60, '1d': 24*60*60, '3d': 3*24*60*60,
            '1w': 7*24*60*60
        }

    def pullData(self, endPoint, params=None):
        data = requests.get(self.baseUrl + endPoint, params=params).content.decode('utf-8')
        return json.loads(data)

    def getBTCAssets(self):
        dayStats = self.pullData('/api/v1/ticker/24hr')
        return [stat['symbol'] for stat in dayStats if 'BTC' in stat['symbol']]

    def getUSDTAssets(self):
        dayStats = self.pullData('/api/v1/ticker/24hr')
        return [stat['symbol'] for stat in dayStats if 'USDT' in stat['symbol']]

    def getFirstTrade(self, asset, binSize):
        return self.pullData('/api/v1/klines?symbol=%s&interval=%s&limit=1&startTime=0' %
                        (asset, binSize))[0][0] / 1000

    def list2Dict(self, val):
        return {
            'milliTimestamp': val[0], 'open': val[1], 'high': val[2],
            'low': val[3], 'close': val[4], 'volume': val[5],
            'quoteVol': val[7], 'numTrades': val[8],
            'takerBaseAssetVol': val[9], 'takerQuoteAssetVol': val[10],
            'TS': val[0] / 1000
        }

    def pullCandles(self, asset, binSize, startTime, endTime=None, isDemo=False):
        data = []
        tmpTime = startTime * 1000
        endTime = endTime if endTime else time.time() - self.bin2Time['1d']
        while tmpTime + 500 * self.bin2Time[binSize] < endTime:
            try:
                tmpData = self.pullData('/api/v1/klines?symbol=%s&interval=%s&limit=500&startTime=%s' %
                                   (asset, binSize, startTime))
            except OSError:
                time.sleep(30)
                tmpData = self.pullData('/api/v1/klines?symbol=%s&interval=%s&limit=500&startTime=%s' %
                                   (asset, binSize, startTime))
            tmpTime = tmpData[-1][6] / 1000
            data += [self.list2Dict(val) for val in tmpData]
            time.sleep(1.5)
        lastData = self.pullData('/api/v1/klines?symbol=%s&interval=%s&limit=500&startTime=%s&endTime=%s' %
                            (asset, binSize, tmpTime, endTime * 1000))
        data += [self.list2Dict(val) for val in lastData]
        if not isDemo:
            print('Add mongo implementation')
            self.MU.toMongo(
                data=data, colName='%s_%s' % (asset, binSize), id='milliTimestamp'
            )
        else:
            return pd.DataFrame(
                data, columns=['milliTimestamp', 'open', 'high', 'low', 'close', 'volume', 'quoteVol',
                               'numTrades', 'takerBaseAssetVol', 'takerQuoteAssetVol', 'TS']
            )

    def updateDB(self):
        for asset in self.getBTCAssets() + self.getUSDTAssets():
            print('For asset: %s' % asset)
            for bin in self.bin2Time.keys():
                col = '%s_%s' % (asset, bin)
                startTime = self.MU.lastVal(col) if self.MU.count(col) != 0 else self.getFirstTrade(asset, bin)
                if int(time.time() - self.bin2Time['1d']) - startTime > 1000:
                    print('Starting bin size: %s' % bin)
                    print(self.TU.getDatetime(startTime))
                    self.pullCandles(
                        asset=asset, binSize=bin, startTime=startTime
                    )
                    print('%s updated' % col)
                else:
                    print('Already up to date for bin size: %s' % bin)
