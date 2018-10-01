from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.main.Strategy.Open.lib import *
from Pipeline.main.AssetSelection.Select import Select
from Pipeline.main.Strategy.Open.OpenTrade import OpenTrade
from Pipeline.main.Utils.EmailUtil import EmailUtil
import logging
from pymongo import MongoClient
import time
import Settings
import yaml
from datetime import datetime


class Enter:

    def __init__(self, stratName, isTest=False):
        logging.debug('Initialising Enter()')
        self.compPath = '%s/Pipeline/resources/%s' % (Settings.BASE_PATH, stratName)
        self.stratName = stratName
        with open('%s/config.yml' % self.compPath) as stratFile:
            self.config = yaml.load(stratFile)
        self.enterStrat = eval(self.config['enter']['name'])(stratName=stratName, isTest=isTest)
        self.Select = Select(stratName)
        self.OT = OpenTrade(stratName=stratName, isLive=self.config['isLive'])
        self.pull = Pull()
        self.col = MongoClient('localhost', 27017)[stratName]['currentPositions']

    def runIndiv(self, asset, testData):
        # for testing
        return self.enterStrat.run(asset, exchange='Binance', testData=testData)

    def run(self):
        try:
            logging.info('Starting Enter.run: %s' % datetime.now())
            openList = []
            currentPositions = [val['assetName'] for val in list(self.col.find({}, {'assetName': 1}))]
            assetList = self.Select.assets()
            self.OT.initRun()
            for asset, exchange in [val for val in assetList if val[0] not in currentPositions]:
                logging.debug('Starting asset: %s' % asset)
                if self.enterStrat.run(asset, exchange=exchange, testData=None):
                    logging.info('Entering trade: %s' % asset)
                    openPrice = self.pull.assetPrice(exchange=exchange, asset=asset, dir='buy')
                    if openPrice != -1:
                        openList.append(asset)
                        self.OT.open(assetVals=(asset, exchange, openPrice))
                logging.debug('Debug so as not to ping rate limiters')
                time.sleep(1.5)
            self.OT.updateBooks()
            logging.info('Ending Enter run')
            logging.info('%s assets analysed' % len(assetList))
            logging.info('Entering trades: \n %s' % openList if len(openList) != 0 else '0 trades entered')
        except Exception as e:
            EmailUtil(strat=self.stratName).errorExit(file=self.stratName, funct='Enter.run()', message=e)
            raise Exception

# Enter(db='disco', stratName='CheapVol_ProfitRun').run()