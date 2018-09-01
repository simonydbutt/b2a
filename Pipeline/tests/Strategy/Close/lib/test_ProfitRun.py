from Pipeline.main.Strategy.Close.lib.ProfitRun import ProfitRun
from Pipeline.tests.Strategy.Close.lib.ProfitRunTestData import *
from Pipeline.main.Utils.AddLogger import AddLogger
from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from tinydb import TinyDB, Query
import Settings
import yaml


def before():
    dbPath = 'Pipeline/tests/test_DB'
    CCD = CreateCleanDir(filePathList=['%s/CodeLogs/testProfitRun' % dbPath,
                                       '%s/CurrentPositions' % dbPath])
    CCD.create()
    AL = AddLogger(dirPath='Pipeline/tests/test_DB/CodeLogs/testProfitRun', stratName='testProfitRun')
    P = Pull('Binance', AL.logger)
    db = TinyDB('%s/%s/CurrentPositions/test.ujson' % (Settings.BASE_PATH, dbPath))
    posDataInit = {'assetName': 'ADABTC', 'openPrice': 0.0000158, 'currentPrice': 0.0000158, 'periods': 0,
               'positionSize': 0.4995, 'paperSize': 0.4995, 'TSOpen': 1534711395}
    posDataMain = {'assetName': 'ADABTC', 'openPrice': 0.0000158, 'currentPrice': 0.0000158, 'periods': 0,
               'positionSize': 0.4995, 'paperSize': 0.4995, 'TSOpen': 1534711395, 'hitPrice': 11, 'sellPrice': 9}
    posDataPeriods = {'assetName': 'ADABTC', 'openPrice': 0.0000158, 'currentPrice': 0.0000158, 'periods': 6,
               'positionSize': 0.4995, 'paperSize': 0.4995, 'TSOpen': 1534711395, 'hitPrice': 11, 'sellPrice': 9}
    db.insert(posDataInit)
    db.insert(posDataMain)
    db.insert(posDataPeriods)
    with open('%s/Pipeline/tests/test_DB/Configs/testStrat.yml' % Settings.BASE_PATH) as file:
        params = yaml.load(file)
    PR = ProfitRun(pullData=P, configParams=params, isTest=True)
    return PR, db, CCD, posDataInit, posDataMain, posDataPeriods


def test_updatePostition():
    PR, db, CCD, posDataInit, _, _ = before()
    PR.updatePosition(positionData=posDataInit, db=db, testData=updatePosData)
    doc = db.search(Query().assetName == 'ADABTC')[0]
    assert doc['hitPrice'] == 10.4142
    assert doc['sellPrice'] == 8.2929
    CCD.clean()


def test_profitRun():
    PR, db, CCD, posDataInit, posDataMain, posDataPeriods = before()
    assert not PR.run(positionData=posDataInit, db=db, testPrice=10, testData=updatePosData)[0]
    assert not PR.run(positionData=posDataMain, db=db, testPrice=12, testData=updatePosData)[0]
    assert not PR.run(positionData=posDataMain, db=db, testPrice=10)[0]
    assert PR.run(positionData=posDataMain, db=db, testPrice=8.9)[0]
    assert PR.run(positionData=posDataPeriods, db=db, testPrice=10)[0]
    CCD.clean()


if __name__ == '__main__':
    test_updatePostition()
    test_profitRun()