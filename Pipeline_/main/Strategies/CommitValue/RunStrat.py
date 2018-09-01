from Pipeline_.main.Strategies.CommitValue.GetAssets import GetAssets
from Pipeline_.main.Strategies.OpenClosePosition import OpenClosePosition
from Pipeline_.main.Utils.AddLogger import AddLogger
from tinydb import TinyDB, Query
import uuid
import logging
import Settings
import yaml
import time


class RunStrat:

    """
    """

    def __init__(self, stratName='CommitValue',
                 fileLogLevel=logging.INFO, consoleLogLevel=logging.WARNING,
                 dbPath='Pipeline_/DB',
                 feeDict={'Binance': 0.001, 'HitBTC': 0.001, 'Hadax': 0.002}):
        self.compDBPath = '%s/%s' % (Settings.BASE_PATH, dbPath)
        self.stratName = stratName
        self.baseStratName = stratName
        self.feeDict = feeDict
        self.logger = AddLogger(
            filePath='%s/CodeLogs/%s' % (self.compDBPath, self.baseStratName),
            stratName=self.baseStratName,
            fileLogLevel=fileLogLevel,
            consoleLogLevel=consoleLogLevel
        ).logger
        with open('%s/Configs/%s/%s.yml' % (self.compDBPath, self.baseStratName, self.stratName)) as configFile:
            self.config = yaml.load(configFile)
        self.currentDB = TinyDB('%s/CurrentPositions/%s/%s.ujson' % (
            self.compDBPath, self.baseStratName, self.config['stratID']
        ))
        self.GA = GetAssets(
            logger=self.logger, minCommits=self.config['minCommits'], numAssets=self.config['numPositions']
        )
        self.CO = OpenClosePosition(stratName=stratName, baseStratName=stratName,
                                    fees=feeDict, dbPath=dbPath)
        self.logLists = {
            'Enter': [],
            'Update': [],
            'Close': []
        }
        self.logger.info('Starting CommitValue Strat')

    def getPrice(self, sym, exchange):
        return self.GA.pullExchangeDict[exchange].getAssetPrice('%sBTC' % sym)

    def run(self):
        newPositions = self.GA.allocatePositions()
        currentPositions = {
            val['Symbol']: val for val in
            self.currentDB.all()
        }
        for sym in currentPositions.keys():
            q = Query()
            cP = currentPositions[sym]
            cP['price'] = float(self.getPrice(sym=sym, exchange=cP['Exchange']))
            currentCap = cP['amountHeld'] * cP['price']
            if sym in newPositions.keys():
                # Update Position
                newCap = round(self.CO.capitalDict['liquidCurrent']*newPositions[sym]['Allocate']*
                               (1 - self.feeDict[cP['Exchange']]), 4)
                print(newCap)
                print(self.CO.capitalDict['liquidCurrent'])
                print(newPositions[sym]['Allocate'])
                changeCap = round(currentCap - newCap, 4)
                self.currentDB.update(
                    {
                        'capAllocated': newCap,
                        'amountHeld': newCap / cP['price'],
                        'currentPrice': cP['price'],
                        'periods': cP['periods'] + 1
                     },
                     q.Symbol == sym
                )
                self.logger.info('Updated Position: %s, buying %s BTC' % (cP['AssetName'], changeCap) if changeCap > 0 else
                                 'Updated Position: %s, selling %s BTC' % (cP['AssetName'], -changeCap))
                if changeCap < 0:
                    self.CO.closePosition({
                        'asset': cP['AssetName'],
                        'stratID': self.config['stratID'],
                        'tradeID': cP['tradeID'],
                        'openPrice': cP['buyPrice'],
                        'closePrice': cP['price'],
                        'periods': cP['periods'],
                        'capitalAllocated': cP['capAllocated'],
                        'TSOpen': cP['TSOpen'],
                        'TSClose': round(time.time()),
                        'amountHeld': changeCap,
                        'Exchange': cP['Exchange']
                    })
                else:
                    self.CO.openPosition({'capAllocated': changeCap})
            else:
                # To sell of position
                self.CO.closePosition({
                    'asset': cP['AssetName'],
                    'stratID': self.config['stratID'],
                    'tradeID': cP['tradeID'],
                    'openPrice': cP['buyPrice'],
                    'closePrice': cP['price'],
                    'periods': cP['periods'],
                    'capitalAllocated': cP['capAllocated'],
                    'TSOpen': cP['TSOpen'],
                    'TSClose': round(time.time()),
                    'amountHeld': cP['amountHeld'],
                    'Exchange': cP['Exchange']
                })
                self.currentDB.remove(q.Symbol == sym)
                self.logger.info('Sold Position: %s for %s BTC' % (cP['AssetName'], currentCap))
        # For the new positions not already in
        for sym in newPositions.keys():
            if sym not in currentPositions.keys():
                pos = newPositions[sym]
                buyAmount = round(self.CO.capitalDict['liquidCurrent'] * pos['Allocate'] *
                                  (1-self.feeDict[pos['Exchange']]), 4)
                price = float(self.getPrice(sym, exchange=pos['Exchange']))
                openDict = {
                    'AssetName': pos['Name'],
                    'Symbol': pos['Symbol'],
                    'Exchange': pos['Exchange'],
                    'amountHeld': buyAmount / price,
                    'capAllocated': buyAmount,
                    'tradeID': str(uuid.uuid1()),
                    'currentPrice': price,
                    'buyPrice': price,
                    'TSOpen': round(time.time()),
                    'periods': 1
                }
                self.CO.openPosition(openDict)
                self.currentDB.insert(openDict)
                self.logger.info('Opened Position: %s for %s BTC' % (pos['Name'], buyAmount))


RunStrat(consoleLogLevel=logging.INFO).run()