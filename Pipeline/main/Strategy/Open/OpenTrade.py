from Pipeline.main.PositionSize.Position import Position
from Pipeline.main.Utils.ExchangeUtil import ExchangeUtil
import yaml
import time


class OpenTrade:

    def __init__(self, configParams, compPath, Pull, db, capName='Capital'):
        self.capPath = '%s/%s.yml' % (compPath, capName)
        self.db = db
        self.Pull = Pull
        self.configParams = configParams
        self.EU = ExchangeUtil(self.configParams['enter']['exchange'])
        with open(self.capPath) as capFile:
            self.capDict = yaml.load(capFile)
        self.P = Position(stratConfig=configParams, capConfig=self.capDict)

    def open(self, asset):
        openPrice = self.Pull.assetPrice(symbol=asset, dir='buy')
        capAllocated = round(self.P.getSize(asset=asset), 6)
        openDict = {
            'assetName': asset,
            'openPrice': openPrice,
            'currentPrice': openPrice,
            'periods': 0,
            'positionSize': capAllocated * (1 - self.EU.fees()),
            'TSOpen': round(time.time())
        }
        self.db.insert(openDict)
        self.capDict['paperCurrent'] -= round(capAllocated - openDict['positionSize'], 6)
        self.capDict['liquidCurrent'] -= capAllocated

    def updateBooks(self):
        self.capDict['percentAllocated'] = round(1 - self.capDict['liquidCurrent']/self.capDict['paperCurrent'], 3)
        self.capDict['paperPnL'] = round(self.capDict['paperCurrent'] / self.capDict['initialCapital'], 3)
        with open(self.capPath, 'w') as capFile:
            yaml.dump(self.capDict, capFile)
