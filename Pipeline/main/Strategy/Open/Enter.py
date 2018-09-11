from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.main.Strategy.Open.lib import *
from Pipeline.main.AssetSelection.Select import Select
from Pipeline.main.Strategy.Open.OpenTrade import OpenTrade
import logging
from pymongo import MongoClient
import time
import Settings
import yaml
from datetime import datetime


class Enter:

    def __init__(self, stratName, isTest=False):
        self.compPath = '%s/Pipeline/resources/%s' % (Settings.BASE_PATH, stratName)
        with open('%s/config.yml' % self.compPath) as stratFile:
            self.configParams = yaml.load(stratFile)
        self.enterStrat = eval(self.configParams['enter']['name'])(params=self.configParams, isTest=isTest)
        self.Select = Select(config=self.configParams)
        self.OT = OpenTrade(stratName=stratName)
        self.db = MongoClient('localhost', 27017)[stratName]

    def runIndiv(self, asset, Pull, testData):
        # for testing
        return self.enterStrat.run(asset, Pull=Pull, testData=testData)

    def run(self):
        openList = []
        logging.info('Starting Enter run: %s' % datetime.now())
        currentPositions = [val['assetName'] for val in list(self.db['currentPositions'].find({}, {'assetName': 1}))]
        assetList = self.Select.assets()
        for asset, exchange in [val for val in assetList if val[0] not in currentPositions]:
            logging.debug('Starting asset: %s' % asset)
            pull = Pull(exchange=exchange)
            if self.enterStrat.run(asset, Pull=pull, testData=None):
                logging.info('Entering trade: %s' % asset)
                openPrice = pull.assetPrice(asset=asset, dir='buy')
                if openPrice != -1:
                    openList.append(asset)
                    self.OT.open(assetVals=(asset, exchange, openPrice))
            logging.debug('Debug so as not to ping rate limiters')
            time.sleep(1)
        self.OT.updateBooks()
        logging.info('Ending Enter run')
        logging.info('%s assets analysed' % len(assetList))
        logging.info('Entering trades: \n %s' % openList if len(openList) != 0 else '0 trades entered')


# Enter(db='disco', stratName='CheapVol_ProfitRun').run()