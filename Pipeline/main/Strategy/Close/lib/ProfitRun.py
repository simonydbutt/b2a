from tinydb import Query
import numpy as np


class ProfitRun:
    """
        If config != hitPrice/sellPrice then calc as first run
        Trailing stop based on standard deviation levels.
        Sells if price goes below 'sellPrice'
        'sellPrice' increases is close > 'hitPrice'
    """

    def __init__(self, configParams, pullData, isTest=False):
        self.isTest = isTest
        self.configParams = configParams['exit']
        self.Pull = pullData

    def updatePosition(self, positionData, db, testData=None):
        data = self.Pull.candles(asset=positionData['assetName'], limit=self.configParams['maPeriods'], lastReal=True,
                                 interval=self.configParams['granularity'], columns=['close']) if \
            not self.isTest else testData
        ma, std = np.mean(data['close']), np.std(data['close'])
        db.update(
            {
                'hitPrice': np.round(ma + self.configParams['stdDict']['up']*std, 4),
                'sellPrice': np.round(ma - self.configParams['stdDict']['down']*std, 4)
            }, Query().assetName == positionData['assetName']
        )

    def run(self, positionData, db, testPrice=None, testData=None):
        price = self.Pull.assetPrice(positionData['assetName']) if not self.isTest else testPrice
        if 'hitPrice' not in positionData.keys():
            self.updatePosition(positionData=positionData, db=db, testData=None if not self.isTest else testData)
            return False, price
        else:
            if positionData['periods'] > self.configParams['closePeriods']:
                return True, price
            elif price > positionData['hitPrice']:
                self.updatePosition(positionData=positionData, db=db, testData=None if not self.isTest else testData)
                return False, price
            elif price < positionData['sellPrice']:
                return True, price
            else:
                return False, price
