from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.main.Strategy.Open.lib import *
from Pipeline.main.Strategy.Open.OpenTrade import OpenTrade
from tinydb import TinyDB
import Settings
import yaml


class Enter:

    def __init__(self, stratName, logger, dbPath='Pipeline/DB', isTest=False):
        self.compPath = '%s/%s' % (Settings.BASE_PATH, dbPath)
        with open('%s/Configs/%s.yml' % (self.compPath, stratName)) as stratFile:
            self.configParams = yaml.load(stratFile)
        self.db = TinyDB('%s/CurrentPositions/%s.ujson' % (self.compPath, stratName))
        self.currentPositions = [val['assetName'] for val in self.db.all()]
        self.Pull = Pull(exchange=self.configParams['enter']['exchange'], logger=logger)
        self.enterStrat = eval(self.configParams['enter']['name'])(params=self.configParams, pullData=self.Pull,
                                                                   isTest=isTest)
        self.logger = logger

    def runIndiv(self, asset, testData):
        # for testing
        return self.enterStrat.run(asset, testData=testData)

    def run(self):
        openList = []
        self.logger.info('Starting Enter run')
        OT = OpenTrade(self.configParams, compPath=self.compPath, db=self.db, Pull=self.Pull)
        allAssetsList = self.Pull.BTCAssets() if self.configParams['assetList'] == 'all' else self.configParams['assetList']
        for asset in [val for val in allAssetsList if val not in self.currentPositions]:
            self.logger.debug('Starting asset: %s' % asset)
            if self.enterStrat.run(asset, testData=None):
                self.logger.info('Entering trade: %s' % asset)
                openList.append(asset)
                OT.open(asset)
            else:
                self.logger.info('No action for asset: %s' % asset)
        OT.updateBooks()
        self.db.close()
        self.logger.info('Ending Enter run')
        self.logger.info('%s assets analysed' % len(allAssetsList))
        self.logger.info('Entering trades: \n %s' % openList if len(openList) != 0 else '0 trades entered')


# from Pipeline.main.Utils.AddLogger import AddLogger
# import logging
# AL = AddLogger(dirPath='Pipeline/DB/CodeLogs/CheapVol_ProfitRun', stratName='CheapVol_ProfitRun', consoleLogLevel=logging.DEBUG)
# Enter(stratName='CheapVol_ProfitRun', logger=AL.logger).run()