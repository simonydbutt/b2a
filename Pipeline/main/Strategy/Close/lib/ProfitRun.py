from tinydb import Query
import numpy as np


class ProfitRun:
    """
        If config != hitPrice/sellPrice then calc as first run
        Trailing stop based on standard deviation levels.
        Sells if price goes below 'sellPrice'
        'sellPrice' increases is close > 'hitPrice'

        Config Requirements:
            - maPeriods
            - stdDict
                - up
                - down
            - closePeriods
    """

    def __init__(self, configParams, isTest=False):
        self.isTest = isTest
        self.configParams = configParams['exit']

    def updatePosition(self, positionData, db, Pull, testData=None):
        data = Pull.candles(asset=positionData['assetName'], limit=self.configParams['maPeriods'], lastReal=True,
                            interval=self.configParams['granularity'], columns=['close']) if not self.isTest else testData
        ma, std = np.mean(data['close']), np.std(data['close'])
        db.update(
            {
                'hitPrice': np.round(positionData['currentPrice'] + self.configParams['stdDict']['up']*std, 8),
                'sellPrice': np.round(positionData['currentPrice'] - self.configParams['stdDict']['down']*std, 8)
            }, Query().assetName == positionData['assetName']
        )

    def run(self, positionData, db, Pull, testPrice=None, testData=None):
        price = Pull.assetPrice(positionData['assetName']) if not self.isTest else testPrice
        if 'hitPrice' not in positionData.keys():
            self.updatePosition(positionData=positionData, db=db, Pull=Pull,
                                testData=None if not self.isTest else testData)
            return False, price
        else:
            if positionData['periods'] > self.configParams['closePeriods']:
                return True, price
            elif price > positionData['hitPrice']:
                self.updatePosition(positionData=positionData, db=db, Pull=Pull,
                                    testData=None if not self.isTest else testData)
                return False, price
            elif price < positionData['sellPrice']:
                return True, price
            else:
                return False, price
