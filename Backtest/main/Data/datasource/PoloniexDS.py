from Backtest.main.Utils.MongoUtil import MongoUtil
from Backtest.main.Utils.TimeUtil import TimeUtil
import pandas as pd
import json
import requests
import time


class PoloniexDS:

    """
        Datasource for Poloniex exchanges
        Mostly to use to backtest binance strats

        For time being only pulling grans: 7200, 14400, 86400 (2h, 4h, 1d)
        If create a decent 5, 15 or 30 min strat, will pull (and change pullCandles)
    """

    def __init__(self):
        self.MU = MongoUtil(dbName='poloniex')
        self.TU = TimeUtil()
        self.baseUrl = 'https://poloniex.com/public?command='

    def pullData(self, endPoint, params=None):
        data = requests.get(self.baseUrl + endPoint, params=params).content.decode('utf-8')
        return json.loads(data)

    def getBTCAssets(self):
        pairList = self.pullData(endPoint='returnTicker')
        return [pair for pair in pairList if 'BTC_' in pair]

    def pullCandles(self, asset, binSize, startTime=1262304000, endTime=None, isDemo=False):
        gran = self.TU.bin2TS[binSize]
        data = None
        endPointUrl = 'returnChartData&currencyPair=%s&start=%s&end=%s&period=%s' % (asset, startTime, endTime, gran) if \
            endTime else 'returnChartData&currencyPair=%s&start=%s&period=%s' % (asset, startTime, gran)
        try:
            data = self.pullData(endPointUrl)
        except OSError:
            time.sleep(30)
            data = self.pullData(endPointUrl)
        if data:
            if not isDemo:
                self.MU.toMongo(
                    data=data, colName='%s_%s' % (asset.replace('_', ''), binSize), id='date', parameters={'TS': 'date'}
                )
            else:
                return pd.DataFrame(data)

    def updateDB(self):
        for asset in self.getBTCAssets():
            print('For asset: %s' % asset.replace('_', ''))
            for bin in ('2h', '4h', '1d'):
                col = '%s_%s' % (asset.replace('_', ''), bin)
                startTime = self.MU.lastVal(col) if self.MU.count(col) != 0 else 1262304000
                if int(time.time() - self.TU.bin2TS['1d']) - startTime > 1000:
                    print('Starting pull of bin size: %s' % bin)
                    self.pullCandles(
                        asset=asset, binSize=bin, startTime=startTime, endTime=1496275200
                    )
                    self.MU.index(colName=col)
                    print('%s updated' % col)
                else:
                    print('Already up to date for col: %s' % col)

    def createCSV(self, asset, binSize, startTime=1262304000, location='../csv/', endTime=None):
        df = self.pullCandles(asset=asset, binSize=binSize, startTime=startTime, endTime=endTime, isDemo=True)
        df.to_csv('%s%s.csv' % (location, asset), compression='gzip')

