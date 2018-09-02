from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.main.Strategy.Open.lib import *
from Pipeline.main.AssetSelection.Select import Select
from Pipeline.main.Strategy.Open.OpenTrade import OpenTrade
from tinydb import TinyDB
import Settings
import yaml


class Enter:

    def __init__(self, logger, dbPath, isTest=False):
        self.compPath = '%s/%s' % (Settings.BASE_PATH, dbPath)
        with open('%s/config.yml' % self.compPath) as stratFile:
            self.configParams = yaml.load(stratFile)
        self.db = TinyDB('%s/currentPositions.ujson' % self.compPath)
        self.enterStrat = eval(self.configParams['enter']['name'])(params=self.configParams, isTest=isTest)
        self.logger = logger
        self.Select = Select(config=self.configParams, logger=self.logger)

    def runIndiv(self, asset, Pull, testData):
        # for testing
        return self.enterStrat.run(asset, Pull=Pull, testData=testData)

    def run(self):
        openList = []
        self.logger.info('Starting Enter run')
        currentPositions = [val['assetName'] for val in self.db.all()]
        OT = OpenTrade(self.configParams, compPath=self.compPath, db=self.db)
        assetList = self.Select.assets()
        for asset, exchange in [val for val in assetList if val[0] not in currentPositions]:
            pull = Pull(exchange=exchange, logger=self.logger)
            self.logger.debug('Starting asset: %s' % asset)
            if self.enterStrat.run(asset, Pull=pull, testData=None):
                self.logger.info('Entering trade: %s' % asset)
                openList.append(asset)
                OT.open(assetVals=(asset, exchange), Pull=pull)
            else:
                self.logger.info('No action for asset: %s' % asset)
        OT.updateBooks()
        self.db.close()
        self.logger.info('Ending Enter run')
        self.logger.info('%s assets analysed' % len(assetList))
        self.logger.info('Entering trades: \n %s' % openList if len(openList) != 0 else '0 trades entered')
