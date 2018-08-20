from tinydb import Query
import numpy as np


class ProfitRun:
    """
        If config != hitPrice/sellPrice then calc as first run
        Trailing stop based on standard deviation levels.
        Sells if price goes below 'sellPrice'
        'sellPrice' increases is close > 'hitPrice'
    """

    def __init__(self, configParams, pullData, db, isTest=False):
        self.isTest = isTest
        self.configParams = configParams['exit']
        self.Pull = pullData
        self.db = db

    def updatePosition(self, positionData):
        data = self.Pull.candles(asset=positionData['assetName'], limit=self.configParams['maPeriods'],
                                 interval=self.configParams['granularity'], lastReal=True)
        ma, std = np.mean(data['close']), np.std(data['close'])
        self.db.update(
            {
                'hitPrice': ma + self.configParams['stdDict']['up'],
                'sellPrice': ma - self.configParams['stdDict']['down']
            }, Query().assetName == positionData['assetName']
        )

    def run(self, positionData, testData=None):
        price = self.Pull.assetPrice(positionData['assetName'])
        if 'hitPrice' not in positionData.keys():
            self.updatePosition(positionData=positionData)
            return False, price
        else:
            if positionData['periods'] > self.configParams['closePeriods']:
                return True, price
            elif price > positionData['hitPrice']:
                self.updatePosition(positionData=positionData)
                return False, price
            elif price < positionData['sellPrice']:
                return True, price
            else:
                return False, price
