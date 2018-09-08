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
from datetime import datetime


class Enter:

    def __init__(self, db, stratName, isTest=False):
        self.compPath = '%s/Pipeline/DB/%s/%s' % (Settings.BASE_PATH, db, stratName)
        with open('%s/config.yml' % self.compPath) as stratFile:
            self.configParams = yaml.load(stratFile)
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
        print('Starting Enter run: %s' % datetime.now())
        db = TinyDB('%s/currentPositions.ujson' % self.compPath)
        currentPositions = [val['assetName'] for val in db.all()]
        OT = OpenTrade(self.configParams, compPath=self.compPath, db=db)
        assetList = self.Select.assets()
        for asset, exchange in [val for val in assetList if val[0] not in currentPositions]:
            pull = Pull(exchange=exchange, logger=self.AL.logger)
            if self.enterStrat.run(asset, Pull=pull, testData=None):
                print('Entering trade: %s' % asset)
                openPrice = pull.assetPrice(symbol=asset, dir='buy')
                if openPrice != -1:
                    openList.append(asset)
                    OT.open(assetVals=(asset, exchange, openPrice))
            time.sleep(1)
        OT.updateBooks()
        db.close()
        print('Ending Enter run')
        print('%s assets analysed' % len(assetList))
        print('Entering trades: \n %s' % openList if len(openList) != 0 else '0 trades entered')


# Enter(db='disco', stratName='CheapVol_ProfitRun').run()