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
        self.bin2TS = self.TU.bin2TS

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
        endTime = endTime*1000 if endTime else (time.time() - self.bin2TS['1d'])*1000
        while tmpTime + 500 * self.bin2TS[binSize]*1000 < endTime:
            tmpData = []
            print(tmpTime + 500 * self.bin2TS[binSize] * 1000 - endTime)
            try:
                tmpData = self.pullData('/api/v1/klines?symbol=%s&interval=%s&limit=500&startTime=%s' %
                                   (asset, binSize, int(tmpTime)))
            except OSError:
                time.sleep(30)
                tmpData = self.pullData('/api/v1/klines?symbol=%s&interval=%s&limit=500&startTime=%s' %
                                   (asset, binSize, int(tmpTime)))
            tmpTime = tmpData[-1][6]
            data += [self.list2Dict(val) for val in tmpData]
            time.sleep(2)
        lastData = self.pullData('/api/v1/klines?symbol=%s&interval=%s&limit=500&startTime=%s&endTime=%s' %
                            (asset, binSize, int(tmpTime), int(endTime)))
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
        for asset in self.getUSDTAssets(): #+ self.getBTCAssets():
            print('For asset: %s' % asset)
            for bin in self.bin2TS.keys():
                col = '%s_%s' % (asset, bin)
                startTime = self.MU.lastVal(col) if self.MU.count(col) != 0 else self.getFirstTrade(asset, bin)
                if int(time.time() - self.bin2TS['1d']) - startTime > 1000:
                    print('Starting pull of bin size: %s' % bin)
                    print(self.TU.getDatetime(startTime))
                    self.pullCandles(
                        asset=asset, binSize=bin, startTime=startTime
                    )
                    self.MU.index(colName=col)
                    print('%s updated' % col)
                else:
                    print('Already up to date for bin size: %s' % bin)

    def createCSV(self, asset, binSize, startTime, location='../csv/', endTime=None):
        df = self.pullCandles(asset=asset, binSize=binSize, startTime=startTime,
                              endTime=endTime, isDemo=True)
        df.to_csv('%s%s.csv.gz' % (location, asset), compression='gzip', index=False)


BinanceDS().createCSV('XMRBTC', '1d', startTime=1514764800, endTime=1514764800+86400)