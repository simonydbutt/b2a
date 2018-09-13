from Pipeline.main.Strategy.Close.lib.ProfitRun import ProfitRun
from Pipeline.tests.Strategy.Close.lib.ProfitRunTestData import *
from Pipeline.main.Utils.AddLogger import AddLogger
from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from tinydb import TinyDB, Query
import Settings
import yaml
# *TODO tomorrow finish this!


def before():
    dbPath = 'Pipeline/DB/test'
    P = Pull('Binance')
    db = TinyDB('%s/%s/currentPositions.ujson' % (Settings.BASE_PATH, dbPath))
    posDataInit = {'assetName': 'ADABTC', 'openPrice': 0.0000158, 'currentPrice': 9, 'periods': 0,
                   'positionSize': 0.4995, 'paperSize': 0.4995, 'TSOpen': 1534711395}
    posDataMain = {'assetName': 'ADABTC', 'openPrice': 0.0000158, 'currentPrice': 0.0000158, 'periods': 0,
                   'positionSize': 0.4995, 'paperSize': 0.4995, 'TSOpen': 1534711395, 'hitPrice': 11, 'sellPrice': 9}
    posDataPeriods = {'assetName': 'ADABTC', 'openPrice': 0.0000158, 'currentPrice': 0.0000158, 'periods': 6,
                      'positionSize': 0.4995, 'paperSize': 0.4995, 'TSOpen': 1534711395, 'hitPrice': 11, 'sellPrice': 9}
    db.insert(posDataInit)
    db.insert(posDataMain)
    db.insert(posDataPeriods)
    params = {'exit': {
        'bolStd': 2, 'granularity': 7200, 'name': ProfitRun, 'maPeriods': 5, 'closePeriods': 5,
        'stdDict': {'up': 1, 'down': 0.5}}
    }
    PR = ProfitRun(configParams=params, isTest=True)
    return PR, db, CCD, posDataInit, posDataMain, posDataPeriods, P


def test_updatePostition():
    PR, db, CCD, posDataInit, _, _, P = before()
    PR.updatePosition(positionData=posDataInit, db=db, testData=updatePosData, Pull=P)
    doc = db.search(Query().assetName == 'ADABTC')[0]
    assert round(doc['hitPrice'], 4) == 10.4142
    assert round(doc['sellPrice'], 4) == 8.2929
    CCD.clean()


def test_profitRun():
    PR, db, CCD, posDataInit, posDataMain, posDataPeriods, P = before()
    assert not PR.run(positionData=posDataInit, db=db, testPrice=10, testData=updatePosData, Pull=P)[0]
    assert not PR.run(positionData=posDataMain, db=db, testPrice=12, testData=updatePosData, Pull=P)[0]
    assert not PR.run(positionData=posDataMain, db=db, testPrice=10, Pull=P)[0]
    assert PR.run(positionData=posDataMain, db=db, testPrice=8.9, Pull=P)[0]
    assert PR.run(positionData=posDataPeriods, db=db, testPrice=10, Pull=P)[0]
    CCD.clean()


if __name__ == '__main__':
    test_updatePostition()
    test_profitRun()
