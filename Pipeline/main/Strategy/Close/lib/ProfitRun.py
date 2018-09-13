from pymongo import MongoClient
import numpy as np
import yaml


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

    def __init__(self, stratName, isTest=False):
        self.isTest = isTest
        with open('%s/Pipeline/resources/%s/config.yml', 'w') as configFile:
            self.configParams = yaml.load(configFile)['exit']
        self.col = MongoClient('localhost', 27017)[stratName]['currentPositions']

    def updatePosition(self, positionData, Pull, testData=None):
        data = Pull.candles(asset=positionData['assetName'], limit=self.configParams['maPeriods'], lastReal=True,
                            interval=self.configParams['granularity'], columns=['close']) if not self.isTest else testData
        ma, std = np.mean(data['close']), np.std(data['close'])
        positionData['hitPrice'] = np.round(positionData['currentPrice'] + self.configParams['stdDict']['up']*std, 8),
        positionData['sellPrice'] = np.round(positionData['currentPrice'] - self.configParams['stdDict']['down']*std, 8)
        self.col.find_one_and_replace({'assetName': positionData['assetName']}, positionData)

    def run(self, positionData, db, Pull, testPrice=None, testData=None):
        price = Pull.assetPrice(positionData['assetName']) if not self.isTest else testPrice
        if 'hitPrice' not in positionData.keys():
            self.updatePosition(positionData=positionData, Pull=Pull, testData=None if not self.isTest else testData)
            return False, price
        else:
            if positionData['periods'] > self.configParams['closePeriods']:
                return True, price
            elif price > positionData['hitPrice']:
                self.updatePosition(positionData=positionData, Pull=Pull, testData=None if not self.isTest else testData)
                return False, price
            elif price < positionData['sellPrice']:
                return True, price
            else:
                return False, price

# *TODO: logging