from pymongo import MongoClient
from Backtest.main.Utils.TimeUtil import TimeUtil
import pandas as pd
import time
import json
import requests


class BitmexDS:

    """
        Datasource for Bitmex exchange
        TODO: initialProp
        TODO: updateData
    """

    def __init__(self):
        self.TU = TimeUtil()
        self.baseUrl = 'https://www.bitmex.com/api/v1/'
        self.bin2Time = {
            '1m': 60,
            '5m': 60 * 5,
            '1h': 60 * 60,
            '1d': 60 * 60 * 24
        }
        self.data = []
        self.db = MongoClient('localhost', 27017)['bitmex']

    def pullData(self, endPoint, params=None):
        data = requests.get(self.baseUrl + endPoint, params=params).content.decode('utf-8')
        return json.loads(data)

    def toMongo(self, data, colName, binSize):
        for val in data:
            if len(list(self.db[colName].find({
                'timestamp': val['timestamp']
            }))) == 0:
                val['binSize'] = self.bin2Time[binSize]
                self.db[colName].insert_one(val)

    def getInst(self):
        return [inst['symbol'] for inst in self.pullData('instrument/active')]

    def getCandles(self, asset, binSize, startTime, endTime, isDemo=False):
        data = []
        tmpTime = startTime
        endTS = self.TU.getTS(endTime)
        while self.TU.getTS(tmpTime) + 500 * self.bin2Time[binSize] < endTS:
            try:
                tmpData = self.pullData('trade/bucketed?binSize=%s&symbol=%s&count=500&startTime=%s' %
                                        (binSize, asset, tmpTime))
            except OSError:
                time.sleep(30)
                tmpData = self.pullData('trade/bucketed?binSize=%s&symbol=%s&count=500&startTime=%s' %
                                        (binSize, asset, tmpTime))
            tmpTime = tmpData[-1]['timestamp']
            data += tmpData
            time.sleep(2)
        data += self.pullData(
            'trade/bucketed?binSize=%s&symbol=%s&count=500&startTime=%s&endTime=%s' %
            (binSize, asset, tmpTime, endTime))
        if not isDemo:
            self.toMongo(
                data=data, colName='%s_%s' % (asset, binSize), binSize=binSize
            )
        else:
            df = pd.DataFrame(data, columns=['timestamp', 'symbol', 'open', 'high', 'low', 'close', 'trades', 'volume',
                                               'vmap', 'lastSize', 'turnover', 'homeNotional', 'foreignNotional']
                              ).drop_duplicates('timestamp')
            df['binSize'] = self.bin2Time[binSize]
            return df
