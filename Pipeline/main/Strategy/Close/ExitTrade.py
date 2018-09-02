from Pipeline.main.Utils.ExchangeUtil import ExchangeUtil
from tinydb import TinyDB, Query
import yaml
import time


class ExitTrade:

    def __init__(self, compPath, stratName, db, capName='capital'):
        self.compPath = compPath
        self.db = db
        with open('%s/%s.yml' % (self.compPath, capName)) as capFile:
            self.capDict = yaml.load(capFile)
        self.transDB = TinyDB('%s/TransactionLogs/%s.ujson' % (compPath, stratName))

    def exit(self, positionDict, currentPrice):
        fees = ExchangeUtil().fees(exchange=positionDict['exchange'])
        exitPositionSize = round((currentPrice/positionDict['openPrice'])*positionDict['positionSize']*(1 - fees),6)
        realPnL = exitPositionSize - positionDict['positionSize']
        self.db.remove(Query().assetName == positionDict['assetName'])
        self.transDB.insert(
            {
                'assetName': positionDict['assetName'],
                'openPrice': positionDict['openPrice'],
                'closePrice': currentPrice,
                'percentPnL': currentPrice/positionDict['openPrice'] - 1,
                'TSOpen': positionDict['TSOpen'],
                'TSClose': round(time.time()),
                'periods': positionDict['periods'] + 1,
                'positionSize': positionDict['positionSize'],
                'realPnL': realPnL
            }
        )
        self.capDict['liquidCurrent'] += exitPositionSize

    def paperValue(self):
        return sum(
            [val['paperSize'] for val in self.db.all()]
        )

    def updateBooks(self):
        self.capDict['paperCurrent'] = round(self.capDict['liquidCurrent'] + self.paperValue(), 4)
        self.capDict['percentAllocated'] = round(1 - self.capDict['liquidCurrent'] / self.capDict['paperCurrent'], 3)
        self.capDict['paperPnL'] = round(self.capDict['paperCurrent'] / self.capDict['initialCapital'], 3)
        self.capDict['liquidCurrent'] = round(self.capDict['liquidCurrent'], 4)
        with open('%s/Capital.yml' % self.compPath, 'w') as capFile:
            yaml.dump(self.capDict, capFile)
