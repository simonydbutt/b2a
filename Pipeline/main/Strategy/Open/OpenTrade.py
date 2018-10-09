from Pipeline.main.PositionSize.Position import Position
from Pipeline.main.Utils.ExchangeUtil import ExchangeUtil
from Pipeline.main.Utils.AccountUtil import AccountUtil
from Pipeline.main.Utils.EmailUtil import EmailUtil
from Pipeline.main.PullData.Price.Pull import Pull
from pymongo import MongoClient
import logging
import Settings
import yaml
import time


class OpenTrade:

    def __init__(self, stratName, isLive=False):
        self.stratName = stratName
        logging.debug('Initialising OpenTrade()')
        self.isLive = isLive
        self.resourcePath = '%s/Pipeline/resources/%s' % (Settings.BASE_PATH, stratName)
        self.db = MongoClient('localhost', 27017)[stratName]
        self.EU = ExchangeUtil()
        self.P = Position(stratName)
        self.pull = Pull()
        self.capDict = None

    def initRun(self):
        with open('%s/capital.yml' % self.resourcePath) as capFile:
            self.capDict = yaml.load(capFile)

    def _getPrice(self, fills):
        return round(sum([float(val['price']) * float(val['qty']) for val in fills])/\
                     sum([float(val['qty']) for val in fills]), 8)

    def open(self, assetVals):
        logging.debug('Starting OpenTrade.open')
        # assetVals = (name, exchange, price)
        capAllocated = self.P.getSize(asset=assetVals[0])
        posSize = capAllocated * (1 - self.EU.fees(exchange=assetVals[1]))
        if not self.isLive:
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
        else:
            try:
                quantity = round(capAllocated / assetVals[2], 2)
                orderDict = self.pull.makeTrade(exchange=assetVals[1], asset=assetVals[0], quantity=quantity, dir='BUY')
                buyPrice = self._getPrice(orderDict['fills'])
                openDict = {
                    'assetName': assetVals[0],
                    'openPrice': buyPrice,
                    'currentPrice': buyPrice,
                    'periods': 0,
                    'positionSize': orderDict['cummulativeQuoteQty'],
                    'posSizeBase': orderDict['executedQty'],
                    'TSOpen': round(time.time()),
                    'exchange': assetVals[1],
                    'clientOrderId': orderDict['clientOrderId']
                }
            except KeyError as e:
                EmailUtil(strat=self.stratName).errorExit(file=self.stratName, funct='Enter.runNorm()', message=e)
                raise Exception('Failed with error message: %s and assetVals: %s' % (e, assetVals))
        self.db['currentPositions'].insert_one(openDict)
        self.capDict['paperCurrent'] -= round(capAllocated - openDict['positionSize'], 6)
        self.capDict['liquidCurrent'] -= capAllocated

    def updateBooks(self):
        logging.debug('Starting OpenTrade.updateBooks()')
        if not self.isLive:
            self.capDict['percentAllocated'] = round(1 - self.capDict['liquidCurrent']/self.capDict['paperCurrent'], 3)
            self.capDict['paperPnL'] = round(self.capDict['paperCurrent'] / self.capDict['initialCapital'], 3)
        else:
            # **TODO hard coding 'Binance' as whole capDict system will need to change to capListDict when adding multiple
            self.capDict = AccountUtil(exchange='Binance').getValue(initCapital=self.capDict['initialCapital'])
        with open('%s/capital.yml' % self.resourcePath, 'w') as capFile:
            yaml.dump(self.capDict, capFile)
