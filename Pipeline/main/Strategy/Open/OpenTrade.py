from Pipeline.main.PositionSize.Position import Position
from Pipeline.main.Utils.ExchangeUtil import ExchangeUtil
from pymongo import MongoClient
import logging
import Settings
import yaml
import time


class OpenTrade:

    def __init__(self, stratName):
        self.resourcePath = '%s/Pipeline/resources/%s' % (Settings.BASE_PATH, stratName)
        self.db = MongoClient('localhost', 27017)[stratName]
        self.EU = ExchangeUtil()
        with open('%s/config.yml' % self.resourcePath) as configFile:
            configParams = yaml.load(configFile)
        with open('%s/capital.yml' % self.resourcePath) as capFile:
            self.capDict = yaml.load(capFile)
        self.P = Position(stratConfig=configParams, capConfig=self.capDict)

    def open(self, assetVals):
        logging.debug('Starting OpenTrade.open')
        # assetVals = (name, exchange, price)
        capAllocated = self.P.getSize(asset=assetVals[0])
        posSize = capAllocated * (1 - self.EU.fees(exchange=assetVals[1]))
        openDict = {
            'assetName': assetVals[0],
            'openPrice': assetVals[2],
            'currentPrice': assetVals[2],
            'periods': 0,
            'positionSize': posSize,
            'paperSize': posSize,
            'TSOpen': round(time.time()),
            'exchange': assetVals[1]
        }
        self.db['currentPositions'].insert_one(openDict)
        self.capDict['paperCurrent'] -= round(capAllocated - openDict['positionSize'], 6)
        self.capDict['liquidCurrent'] -= capAllocated

    def updateBooks(self):
        self.capDict['percentAllocated'] = round(1 - self.capDict['liquidCurrent']/self.capDict['paperCurrent'], 3)
        self.capDict['paperPnL'] = round(self.capDict['paperCurrent'] / self.capDict['initialCapital'], 3)
        with open('%s/capital.yml' % self.resourcePath, 'w') as capFile:
            yaml.dump(self.capDict, capFile)
