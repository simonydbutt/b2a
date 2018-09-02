from Pipeline.main.Strategy.Close.lib.ProfitRun import ProfitRun
from Pipeline.tests.Strategy.Close.lib.ProfitRunTestData import updatePosData
from Pipeline.main.Strategy.Close.Exit import Exit
from Pipeline.main.Utils.AddLogger import AddLogger
from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from tinydb import TinyDB, Query
import Settings
import yaml
import os


dbPath = 'Pipeline/DB/test'


def before():
    CCD = CreateCleanDir(filePathList=['%s/testExit' % dbPath, '%s/testExit/CodeLogs' % dbPath])
    CCD.create()
    AL = AddLogger(db='test', stratName='testExit')
    P = Pull('Binance', AL.logger)
    db = TinyDB('%s/%s/currentPositions.ujson' % (Settings.BASE_PATH, dbPath))
    posDataMain = {'assetName': 'ADABTC', 'openPrice': 0.0000158, 'currentPrice': 0.0000158, 'periods': 0,
                   'positionSize': 0.4995, 'paperSize': 0.4995, 'TSOpen': 1534711395, 'hitPrice': 11, 'sellPrice': 9}
    db.insert(posDataMain)
    with open('%s/%s/config.yml' % (Settings.BASE_PATH, dbPath)) as file:
        params = yaml.load(file)
    with open('%s/%s/testExit/config.yml' % (Settings.BASE_PATH, dbPath), 'w') as configFile:
        yaml.dump(params, configFile)
    PR = ProfitRun(configParams=params, isTest=True)
    E = Exit(db='test', stratName='testExit', isTest=True)
    return PR, E, db, CCD, posDataMain, P


def after():
    os.remove('%s/%s/currentPositions.ujson' % (Settings.BASE_PATH, dbPath))


def test_runIndiv():
    PR, E, db, CCD, posDataMain, P = before()
    assert PR.run(positionData=posDataMain, testPrice=10, db=db, Pull=P) == E.runIndiv(positionData=posDataMain,
                                                                                       testPrice=10, db=db, Pull=P)
    CCD.clean()
    after()


if __name__ == '__main__':
    test_runIndiv()
