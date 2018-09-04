from Pipeline.main.Strategy.Close.lib import *
from Pipeline.main.Strategy.Close.UpdatePosition import UpdatePosition
from Pipeline.main.Strategy.Close.ExitTrade import ExitTrade
from Pipeline.main.Utils.ExchangeUtil import ExchangeUtil
from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.main.Utils.AddLogger import AddLogger
from tinydb import TinyDB
import Settings
import yaml


class Exit:

    """

    """

    def __init__(self, db, stratName, isTest=False):
        self.compPath = '%s/Pipeline/DB/%s/%s' % (Settings.BASE_PATH, db, stratName)
        with open('%s/config.yml' % self.compPath) as stratFile:
            self.configParams = yaml.load(stratFile)
        self.AL = AddLogger(db=db, stratName=stratName, fileLogLevel=self.configParams['logging']['file'],
                            consoleLogLevel=self.configParams['logging']['console'])
        self.exitStrat = eval(self.configParams['exit']['name'])(configParams=self.configParams, isTest=isTest)

    def runIndiv(self, positionData, testPrice, db, Pull):
        return self.exitStrat.run(positionData, testPrice=testPrice, db=db, Pull=Pull)

    def run(self):
        self.AL.logger.info('Starting Exit run')
        db = TinyDB('%s/currentPositions.ujson' % self.compPath)
        U = UpdatePosition(db=db)
        E = ExitTrade(compPath=self.compPath, db=db)
        for positionDict in db.all():
            pull = Pull(logger=self.AL.logger, exchange=positionDict['exchange'])
            self.AL.logger.debug('Analysing open position: %s' % positionDict['assetName'])
            isExit, currentPrice = self.exitStrat.run(positionData=positionDict, testData=None, db=db, Pull=pull)
            if isExit:
                E.exit(positionDict=positionDict, currentPrice=currentPrice)
            else:
                U.update(positionDict=positionDict, currentPrice=currentPrice)
        E.updateBooks()
        db.close()
        self.AL.logger.info('Ending Exit Run')


import logging
# dirPath = 'Pipeline/DB/disco'
# Exit(db='disco', stratName='CheapVol_ProfitRun').run()