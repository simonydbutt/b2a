from Pipeline.main.Strategy.Close.lib import *
from Pipeline.main.Strategy.Close.UpdatePosition import UpdatePosition
from Pipeline.main.Strategy.Close.ExitTrade import ExitTrade
from Pipeline.main.Utils.EmailUtil import EmailUtil
from Pipeline.main.PullData.Price.Pull import Pull
from pymongo import MongoClient
import logging
import Settings
import yaml
import datetime


class Exit:

    """

    """

    def __init__(self, stratName, isTest=False):
        logging.debug('Initializing Exit()')
        with open('%s/Pipeline/resources/%s/config.yml' % (Settings.BASE_PATH, stratName)) as stratFile:
            self.config = yaml.load(stratFile)
        self.stratName = stratName
        self.exitStrat = eval(self.config['exit']['name'])(stratName=stratName, isTest=isTest) if \
            'statArb' not in self.config.keys() else None
        self.col = MongoClient('localhost', 27017)[stratName]['currentPositions']
        self.pull = Pull()
        self.updatePosition = UpdatePosition(stratName)
        self.exitTrade = ExitTrade(stratName, isLive=self.config['isLive'])

    def runIndiv(self, positionData, testPrice, Pull):
        return self.exitStrat.run(positionData, testPrice=testPrice, Pull=Pull)

    def run(self):
        self.runArb() if 'statArb' in self.config else self.runNorm()

    def runNorm(self):
        try:
            logging.info('Starting Exit Run: %s' % datetime.datetime.now())
            currentPositions = list(self.col.find())
            logging.info('Open positions: %s' % [val['assetName'] for val in currentPositions])
            self.exitTrade.initBooks()
            for positionDict in currentPositions:
                logging.debug('Analysing open position: %s' % positionDict['assetName'])
                isExit, currentPrice = self.exitStrat.run(positionData=positionDict, testData=None, Pull=self.pull)
                if isExit:
                    logging.info('Exiting positon: %s' % positionDict['assetName'])
                    self.exitTrade.exit(positionDict=positionDict, currentPrice=currentPrice)
                else:
                    self.updatePosition.update(positionDict=positionDict, currentPrice=currentPrice)
            logging.info('Ending Exit Run' if len(currentPositions) != 0 else 'No assets to analyse')
            self.exitTrade.closeOutBooks()
        except Exception as e:
            EmailUtil(strat=self.stratName).errorExit(file=self.stratName, funct='Exit.run()', message=e)
            raise Exception

    def runArb(self):
        if self.col.count() != 0:
            btcPrice = self.pull.assetPrice(exchange='Binance', asset='BTCUSDT')
            btcDict = self.col.find_one({'assetName': 'BTCUSDT'})
            ethPrice = self.pull.assetPrice(exchange='Binance', asset='ETHUSDT')
            ethDict = self.col.find_one({'assetName': 'ETHUSDT'})
            if btcDict['periods'] == self.config['exit']['maxPeriods']:
                self.exitTrade.exit(positionDict=btcDict, currentPrice=btcPrice)
                self.exitTrade.exit(positionDict=ethPrice, currentPrice=ethPrice)
            else:
                self.updatePosition.update(positionDict=btcDict, currentPrice=btcPrice, dir=btcDict['dir'])
                self.updatePosition.update(positionDict=ethDict, currentPrice=ethPrice, dir=ethDict['dir'])

# dirPath = 'Pipeline/DB/disco'
# Exit(db='disco', stratName='CheapVol_ProfitRun').run()
