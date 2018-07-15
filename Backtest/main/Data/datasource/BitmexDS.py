from Backtest.main.Utils.TimeUtil import TimeUtil
from Backtest.main.Utils.MongoUtil import MongoUtil
import pandas as pd
import time
import json
import requests


class BitmexDS:

    """
        Datasource for Bitmex exchange
        TODO: Complete!
    """

    def __init__(self):
        self.TU = TimeUtil()
        self.MU = MongoUtil(dbName='bitmex')
        self.baseUrl = 'https://www.bitmex.com/api/v1/'
        self.bin2Time = {
            '1d': 60 * 60 * 24,
            '1h': 60 * 60,
            '5m': 60 * 5,
            '1m': 60
        }

    def pullData(self, endPoint, params=None):
        data = requests.get(self.baseUrl + endPoint, params=params).content.decode('utf-8')
        return json.loads(data)

    def getInst(self):
        return [inst['symbol'] for inst in self.pullData('instrument/active')]

    def pullCandles(self, asset, binSize, startTime, endTime=None, isDemo=False):
        data = []
        tmpTime = startTime if type(startTime) == str else self.TU.getDatetime(startTime)
        endTS = self.TU.getTS(endTime) if endTime else time.time() - self.bin2Time['1d']
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
        if data != ['error']:
            if not isDemo:
                self.MU.toMongo(
                    data=data, colName='%s_%s' % (asset, binSize),
                    parameters={'binSize': self.bin2Time[binSize], 'TS': ('timestamp', '%Y-%m-%dT%H:%M:%S.000Z')},
                    id='timestamp'
                )
            else:
                df = pd.DataFrame(data, columns=['timestamp', 'symbol', 'open', 'high', 'low', 'close', 'trades', 'volume',
                                                   'vmap', 'lastSize', 'turnover', 'homeNotional', 'foreignNotional']
                              ).drop_duplicates('timestamp')
                df['binSize'] = self.bin2Time[binSize]
                return df
        else:
            print('Error for asset: %s and bin size: %s' % (asset, binSize))

    def updateDB(self):
        for inst in self.getInst():
            print('For instrument: %s' % inst)
            for bin in self.bin2Time.keys():
                col = '%s_%s' % (inst, bin)
                try:
                    print(self.MU.count(col))
                    startTime = self.MU.lastVal(col) if self.MU.count(col) != 0 else \
                    self.TU.getTS(self.pullData('trade/bucketed?binSize=%s&symbol=%s&count=1' % (bin, inst))[0]['timestamp'])
                    if int(time.time() - self.bin2Time['1d']) - startTime > 1000:
                        print('Starting bin size: %s' % bin)
                        print('Start time: %s, End time: %s' % (self.TU.getDatetime(startTime), self.TU.getDatetime(time.time()-self.bin2Time['1d'])))
                        self.pullCandles(
                            asset=inst, binSize=bin,
                            startTime=startTime
                        )
                        self.MU.index(colName=col)
                        print('%s updated' % col)
                    else:
                        print('Already up to date for bin size: %s' % bin)
                except IndexError:
                    print('Not enough date for inst: %s and bin: %s' % (inst, bin))
