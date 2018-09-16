from Pipeline.main.Utils.ExchangeUtil import ExchangeUtil
from Pipeline.main.PullData.Price.Pull import Pull
from pymongo import MongoClient
import Settings
import logging
import yaml
import time


class ExitTrade:

    """
        *TODO: remove hit/sell price after sure all's good
    """

    def __init__(self, stratName):
        logging.debug('Initialising ExitTrade()')
        self.stratName = stratName
        db = MongoClient('localhost', 27017)[stratName]
        self.transCol = db['transactionLogs']
        self.currentCol = db['currentPositions']
        self.pull = Pull()
        self.capDict = None

    def initBooks(self):
        logging.debug('Starting ExitTrade.initBooks')
        with open('%s/Pipeline/resources/%s/capital.yml' % (Settings.BASE_PATH, self.stratName)) as capFile:
            self.capDict = yaml.load(capFile)
        logging.debug('Ending ExitTrade.initBooks')

    def _getPrice(self, fills):
        return round(sum([float(val['price']) * float(val['qty']) for val in fills])/sum([float(val['qty']) for val in fills]), 8)

    def exit(self, positionDict, currentPrice, isSandbox=True):
        logging.debug('Starting ExitTrade.exit')
        fees = ExchangeUtil().fees(exchange=positionDict['exchange'])
        exitPositionSize = round((currentPrice/positionDict['openPrice'])*positionDict['positionSize']*(1 - fees), 6)
        logging.debug('Removing val from db.currentPosition & inserting into db.tranactionLog')
        self.currentCol.delete_one({'assetName': positionDict['assetName']})
        if isSandbox:
            realPnL = exitPositionSize - positionDict['positionSize']
            exitDict = {
                    'assetName': positionDict['assetName'],
                    'openPrice': round(positionDict['openPrice'], 8),
                    'hitPrice': round(positionDict['hitPrice'], 8),
                    'sellPrice': round(positionDict['sellPrice'], 8),
                    'closePrice': round(currentPrice, 8),
                    'percentPnL': round(currentPrice/positionDict['openPrice'] - 1, 6),
                    'TSOpen': positionDict['TSOpen'],
                    'TSClose': round(time.time()),
                    'periods': positionDict['periods'] + 1,
                    'positionSize': positionDict['positionSize'],
                    'realPnL': round(realPnL, 8)
                }
        else:
            orderDict = self.pull.makeTrade(exchange=positionDict['exchange'], asset=positionDict['assetName'],
                                            quantity=positionDict['posSizeBase'], dir='SELL')
            realPnL = orderDict['cummulativeQuoteQty'] - positionDict['cummulativeQuoteQty']
            closePrice = self._getPrice(orderDict['fills'])
            exitDict = {
                'assetName': positionDict['assetName'],
                'openPrice': round(positionDict['openPrice'], 8),
                'hitPrice': round(positionDict['hitPrice'], 8),
                'sellPrice': round(positionDict['sellPrice'], 8),
                'closePrice': closePrice,
                'percentPnL': round(closePrice / positionDict['openPrice'] - 1, 6),
                'TSOpen': positionDict['TSOpen'],
                'TSClose': round(time.time()),
                'periods': positionDict['periods'] + 1,
                'positionSize': positionDict['positionSize'],
                'realPnL': round(realPnL, 8)
            }
        self.transCol.insert_one(exitDict)
        self.capDict['liquidCurrent'] += exitPositionSize
        logging.debug('Ending ExitTrade.run')

    def paperValue(self):
        logging.debug('Starting ExitTrade.paperValue')
        return sum(
            [val['paperSize'] for val in list(self.currentCol.find())]
        )

    def closeOutBooks(self):
        """
        *TODO Base on pull.getAccount and take out to exchange util!
        :return:
        """
        logging.debug('Starting ExitTrade.closeOutBooks')
        self.capDict['paperCurrent'] = round(self.capDict['liquidCurrent'] + self.paperValue(), 4)
        self.capDict['percentAllocated'] = round(1 - self.capDict['liquidCurrent'] / self.capDict['paperCurrent'], 3)
        self.capDict['paperPnL'] = round(self.capDict['paperCurrent'] / self.capDict['initialCapital'], 3)
        self.capDict['liquidCurrent'] = round(self.capDict['liquidCurrent'], 4)
        with open('%s/Pipeline/resources/%s/capital.yml' % (Settings.BASE_PATH, self.stratName), 'w') as capFile:
            yaml.dump(self.capDict, capFile)
        logging.debug('Ending ExitTrade.closeOutBooks')
