from Pipeline.main.Strategy.Close.lib import *
from Pipeline.main.Strategy.Close.UpdatePosition import UpdatePosition
from Pipeline.main.Strategy.Close.ExitTrade import ExitTrade
from Pipeline.main.Utils.ExchangeUtil import ExchangeUtil
from Pipeline.main.PullData.Price.Pull import Pull
from tinydb import TinyDB
import Settings
import yaml


class Exit:

    """

    """

    def __init__(self, stratName, logger, dbPath='Pipeline/DB', isTest=False):
        self.stratName = stratName
        self.compPath = '%s/%s' % (Settings.BASE_PATH, dbPath)
        with open('%s/config.yml' % self.compPath) as stratFile:
            self.configParams = yaml.load(stratFile)
        self.logger = logger
        self.exitStrat = eval(self.configParams['exit']['name'])(configParams=self.configParams, isTest=isTest)

    def runIndiv(self, positionData, testPrice, db, Pull):
        return self.exitStrat.run(positionData, testPrice=testPrice, db=db, Pull=Pull)

    def run(self):
        self.logger.info('Starting Exit run')
        db = TinyDB('%s/currentPositions.ujson' % self.compPath)
        U = UpdatePosition(db=db)
        E = ExitTrade(compPath=self.compPath, db=db, stratName=self.stratName)
        for positionDict in db.all():
            pull = Pull(logger=self.logger, exchange=positionDict['exchange'])
            self.logger.debug('Analysing open position: %s' % positionDict['assetName'])
            isExit, currentPrice = self.exitStrat.run(positionData=positionDict, testData=None, db=db, Pull=pull)
            if isExit:
                print('ExitTrade')
                E.exit(positionDict=positionDict, currentPrice=currentPrice)
            else:
                print('UpdateTrade')
                U.update(positionDict=positionDict, currentPrice=currentPrice)
        E.updateBooks()
        db.close()
        self.logger.info('Ending Exit Run')

