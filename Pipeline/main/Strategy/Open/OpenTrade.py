from Pipeline.main.PositionSize.Position import Position
from Pipeline.main.Utils.ExchangeUtil import ExchangeUtil
import yaml
import time


class OpenTrade:

    def __init__(self, configParams, compPath, db):
        self.capPath = '%s/capital.yml' % compPath
        self.db = db
        self.configParams = configParams
        self.EU = ExchangeUtil()
        with open(self.capPath) as capFile:
            self.capDict = yaml.load(capFile)
        self.P = Position(stratConfig=configParams, capConfig=self.capDict)

    def open(self, assetVals):
        # assetVals = (name, exchange, price)
        capAllocated = round(self.P.getSize(asset=assetVals[0]), 6)
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
        self.db.insert(openDict)
        self.capDict['paperCurrent'] -= round(capAllocated - openDict['positionSize'], 6)
        self.capDict['liquidCurrent'] -= capAllocated

    def updateBooks(self):
        self.capDict['percentAllocated'] = round(1 - self.capDict['liquidCurrent']/self.capDict['paperCurrent'], 3)
        self.capDict['paperPnL'] = round(self.capDict['paperCurrent'] / self.capDict['initialCapital'], 3)
        with open(self.capPath, 'w') as capFile:
            yaml.dump(self.capDict, capFile)
