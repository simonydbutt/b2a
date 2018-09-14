from pymongo import MongoClient
import numpy as np
import Settings
import logging
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
        logging.debug('Initialising ProfitRun()')
        self.isTest = isTest
        with open('%s/Pipeline/resources/%s/config.yml' % (Settings.BASE_PATH, stratName)) as configFile:
            self.configParams = yaml.load(configFile)['exit']
        self.col = MongoClient('localhost', 27017)[stratName]['currentPositions']

    def updatePosition(self, positionData, Pull, testData=None):
        logging.debug('Starting ProfitRun.updatePosition')
        data = Pull.candles(asset=positionData['assetName'], limit=self.configParams['maPeriods'], lastReal=True,
                            interval=self.configParams['granularity'], columns=['close'], exchange=positionData['exchange']) \
            if not self.isTest else testData
        ma, std = np.mean(data['close']), np.std(data['close'])
        positionData['hitPrice'] = np.round(positionData['currentPrice'] + self.configParams['stdDict']['up']*std, 8)
        positionData['sellPrice'] = np.round(positionData['currentPrice'] - self.configParams['stdDict']['down']*std, 8)
        del positionData['_id']
        self.col.find_one_and_replace({'assetName': positionData['assetName']}, positionData)
        logging.debug('Ending ProfitRun.updatePosition')

    def run(self, positionData, Pull, testPrice=None, testData=None):
        logging.debug('Starting ProfitRun.run')
        price = Pull.assetPrice(exchange=positionData['exchange'], asset=positionData['assetName']) if not self.isTest else testPrice
        if 'hitPrice' not in positionData.keys():
            self.updatePosition(positionData=positionData, Pull=Pull, testData=None if not self.isTest else testData)
            logging.debug('Ending ProfitRun.run -> False, price: %s' % price)
            return False, price
        else:
            if positionData['periods'] > self.configParams['closePeriods']:
                logging.debug('Ending ProfitRun.run -> True (timeouts), price: %s' % price)
                return True, price
            elif price > positionData['hitPrice']:
                self.updatePosition(positionData=positionData, Pull=Pull, testData=None if not self.isTest else testData)
                logging.debug('Ending ProfitRun.run -> False, price: %s' % price)
                return False, price
            elif price < positionData['sellPrice']:
                logging.debug('Ending ProfitRun.run -> True (price dip), price: %s' % price)
                return True, price
            else:
                logging.debug('Ending ProfitRun.run -> False, price: %s' % price)
                return False, price
