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
        If ass
    """

    def __init__(self, stratName, logger, dbPath='Pipeline/DB', isTest=False):
        self.stratName = stratName
        self.compPath = '%s/%s' % (Settings.BASE_PATH, dbPath)
        with open('%s/Configs/%s.yml' % (self.compPath, stratName)) as stratFile:
            self.configParams = yaml.load(stratFile)
        self.fees = ExchangeUtil(exchange=self.configParams['exit']['exchange']).fees()
        self.logger = logger
        self.Pull = Pull(exchange=self.configParams['exit']['exchange'], logger=logger)
        self.exitStrat = eval(self.configParams['exit']['name'])(configParams=self.configParams, pullData=self.Pull,
                                                                 isTest=isTest)

    def runIndiv(self, positionData, testPrice):
        return self.exitStrat.run(positionData, testPrice=testPrice)

    def run(self):
        db = TinyDB('%s/CurrentPositions/%s.ujson' % (self.compPath, self.stratName))
        self.logger.info('Starting Exit run')
        U = UpdatePosition(db=self.db)
        E = ExitTrade(compPath=self.compPath, db=self.db, stratName=self.stratName, fees=self.fees)
        for position in self.db.all():
            self.logger.debug('Analysing open position: %s' % position['assetName'])
            isExit, currentPrice = self.exitStrat.run(positionData=position, testData=None, db=db)
            if isExit:
                print('ExitTrade')
                E.exit(positionDict=position, currentPrice=currentPrice)
            else:
                print('UpdateTrade')
                U.update(positionDict=position, currentPrice=currentPrice)
        E.updateBooks()
        db.close()
        self.logger.info('Ending Exit Run')
