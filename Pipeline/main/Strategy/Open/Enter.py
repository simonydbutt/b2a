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

    """
        *TODO Nomics to avoid rate limits
    """

    def __init__(self, stratName, isTest=False, testAssets=None):
        logging.debug('Initialising Enter()')
        self.compPath = '%s/Pipeline/resources/%s' % (Settings.BASE_PATH, stratName)
        self.stratName = stratName
        self.isTest = isTest
        with open('%s/config.yml' % self.compPath) as stratFile:
            self.config = yaml.load(stratFile)
        self.assetList = Select(stratName).assets() if not isTest else testAssets
        self.enterStrat = eval(self.config['enter']['name'])(stratName=stratName, assetList=self.assetList, isTest=isTest)
        self.OT = OpenTrade(stratName=stratName, isLive=self.config['isLive']) if not isTest else None
        self.pull = Pull()
        self.col = MongoClient('localhost', 27017)[stratName]['currentPositions']

    def run(self):
        try:
            logging.info('Starting Enter.run: %s' % datetime.now())
            startTime = time.time()
            openList = []
            currentPositions = [val['assetName'] for val in list(self.col.find({}, {'assetName': 1}))]
            self.OT.initRun() if not self.isTest else None
            self.enterStrat.before() if not self.isTest else None
            for asset, exchange in [val for val in self.assetList if val[0] not in currentPositions]:
                logging.debug('Starting asset: %s' % asset)
                if self.enterStrat.run(asset):
                    logging.info('Entering trade: %s' % asset)
                    openPrice = self.pull.assetPrice(exchange=exchange, asset='%sBTC' % asset, dir='buy') if \
                        not self.isTest else 1
                    if openPrice != -1:
                        openList.append(asset)
                        self.OT.open(assetVals=(asset, exchange, openPrice)) if not self.isTest else None
            self.OT.updateBooks() if not self.isTest else None
            logging.info('Ending Enter run. Took: %s seconds' % round(time.time() - startTime))
            logging.info('%s assets analysed' % len(self.assetList))
            logging.info('Entering trades: \n %s' % openList if len(openList) != 0 else '0 trades entered')
            return openList if self.isTest else None
        except Exception as e:
            EmailUtil(strat=self.stratName).errorExit(file=self.stratName, funct='Enter.runNorm()', message=e)
            raise Exception


# logging.basicConfig(level=logging.DEBUG)
# startTime = time.time()
# E = Enter(stratName='CheapVol_ProfitRun')
# logging.info('\nInit comp, taking: %s seconds\n\n' % round(time.time() - startTime))
# startTime = time.time()
# E.run()
# logging.info('\nRun 1 comp, taking: %s seconds\n\n' % round(time.time() - startTime))
# startTime = time.time()
# E.run()
# logging.info('Run 2 comp, taking: %s seconds' % round(time.time() - startTime))
