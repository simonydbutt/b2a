from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.main.Strategy.Open.lib import *
from Pipeline.main.AssetSelection.Select import Select
from Pipeline.main.Strategy.Open.OpenTrade import OpenTrade
from Pipeline.main.Utils.AddLogger import AddLogger
from tinydb import TinyDB
import time
import Settings
import yaml
import logging


class Enter:

    def __init__(self, db, stratName, isTest=False):
        self.compPath = '%s/Pipeline/DB/%s/%s' % (Settings.BASE_PATH, db, stratName)
        with open('%s/config.yml' % self.compPath) as stratFile:
            self.configParams = yaml.load(stratFile)
        self.db = TinyDB('%s/currentPositions.ujson' % self.compPath)
        self.enterStrat = eval(self.configParams['enter']['name'])(params=self.configParams, isTest=isTest)
        self.AL = AddLogger(stratName=stratName, db=db,
                            consoleLogLevel=self.configParams['logging']['console'],
                            fileLogLevel=self.configParams['logging']['file'])
        self.Select = Select(config=self.configParams, logger=self.AL.logger)

    def runIndiv(self, asset, Pull, testData):
        # for testing
        return self.enterStrat.run(asset, Pull=Pull, testData=testData)

    def run(self):
        openList = []
        self.AL.logger.info('Starting Enter run')
        currentPositions = [val['assetName'] for val in self.db.all()]
        OT = OpenTrade(self.configParams, compPath=self.compPath, db=self.db)
        assetList = self.Select.assets()
        for asset, exchange in [val for val in assetList if val[0] not in currentPositions]:
            pull = Pull(exchange=exchange, logger=self.AL.logger)
            self.AL.logger.info('Starting asset: %s' % asset)
            print(asset)
            if self.enterStrat.run(asset, Pull=pull, testData=None):
                print(1)
                self.AL.logger.warning('Entering trade: %s' % asset)
                openList.append(asset)
                OT.open(assetVals=(asset, exchange), Pull=pull)
            else:
                self.AL.logger.info('No action for asset: %s' % asset)
            # To avoid rate limits...
            # **TODO: look into nomics api
            time.sleep(1)
        OT.updateBooks()
        self.db.close()
        self.AL.logger.info('Ending Enter run')
        self.AL.logger.info('%s assets analysed' % len(assetList))
        self.AL.logger.info('Entering trades: \n %s' % openList if len(openList) != 0 else '0 trades entered')


# Enter(db='disco', stratName='CheapVol_ProfitRun').run()