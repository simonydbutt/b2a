from Pipeline.main.Strategy.Close.lib.ProfitRun import ProfitRun
from Pipeline.tests.Strategy.Close.lib.ProfitRunTestData import updatePosData
from Pipeline.main.Strategy.Close.Exit import Exit
from Pipeline.main.Utils.AddLogger import AddLogger
from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from tinydb import TinyDB, Query
import Settings
import yaml


def before():
    dbPath = 'Pipeline/tests/test_DB'
    CCD = CreateCleanDir(filePathList=['%s/CodeLogs/testExit' % dbPath,
                                       '%s/CurrentPositions' % dbPath])
    CCD.create()
    AL = AddLogger(dirPath='Pipeline/tests/test_DB/CodeLogs/testExit', stratName='testExit')
    P = Pull('Binance', AL.logger)
    db = TinyDB('%s/%s/CurrentPositions/test.ujson' % (Settings.BASE_PATH, dbPath))
    posDataMain = {'assetName': 'ADABTC', 'openPrice': 0.0000158, 'currentPrice': 0.0000158, 'periods': 0,
                   'positionSize': 0.4995, 'paperSize': 0.4995, 'TSOpen': 1534711395, 'hitPrice': 11, 'sellPrice': 9}
    db.insert(posDataMain)
    with open('%s/Pipeline/tests/test_DB/Configs/testStrat.yml' % Settings.BASE_PATH) as file:
        params = yaml.load(file)
    PR = ProfitRun(pullData=P, configParams=params, isTest=True)
    E = Exit(stratName='testStrat', logger=AL.logger, dbPath=dbPath, isTest=True)
    return PR, E, db, CCD, posDataMain


def test_runIndiv():
    PR, E, db, CCD, posDataMain = before()
    assert PR.run(positionData=posDataMain, testPrice=10, db=db) == E.runIndiv(positionData=posDataMain, testPrice=10, db=db)
    CCD.clean()


if __name__ == '__main__':
    test_runIndiv()
