from Pipeline.main.Strategy.Close.ExitTrade import ExitTrade
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from tinydb import TinyDB
import Settings
import yaml
import os


dbPath = 'Pipeline/DB/test'


def before():
    CCD = CreateCleanDir(filePathList=['%s/TransactionLogs' % dbPath])
    CCD.clean()
    CCD.create()
    db = TinyDB('%s/%s/currentPositions.ujson' % (Settings.BASE_PATH, dbPath))
    posDataMain = {'assetName': 'ADABTC', 'openPrice': 10, 'currentPrice': 9, 'periods': 2, 'exchange': 'Binance',
                   'positionSize': 0.4995, 'paperSize': 0.4995, 'TSOpen': 1534711395, 'hitPrice': 11, 'sellPrice': 9}
    posDataSub = {'assetName': 'TESTBTC', 'openPrice': 0.0000158, 'currentPrice': 0.0000158, 'periods': 2,
                  'positionSize': 0.4995, 'paperSize': 0.2, 'TSOpen': 1534711395, 'hitPrice': 11, 'sellPrice': 9,
                  'exchange': 'Binance'}
    db.insert(posDataMain)
    db.insert(posDataSub)
    ET = ExitTrade(compPath='%s/%s' % (Settings.BASE_PATH, dbPath), db=db, stratName='testStrat')
    initCapDict = {
        'initialCapital': 10, 'liquidCurrent': 10, 'paperCurrent': 10,
        'paperPnL': 0, 'percentAllocated': 0
    }
    with open('%s/%s/Capital.yml' % (Settings.BASE_PATH, dbPath), 'w') as capFile:
        yaml.dump(initCapDict, capFile)
    return CCD, db, posDataMain, ET, initCapDict


def test_paperValue():
    CCD, db, _, ET, _ = before()
    assert ET.paperValue() == 0.6995
    CCD.clean()
    after()


def after():
    initCapDict = {
        'initialCapital': 10, 'liquidCurrent': 10, 'paperCurrent': 10,
        'paperPnL': 0, 'percentAllocated': 0
    }
    with open('%s/%s/Capital.yml' % (Settings.BASE_PATH, dbPath), 'w') as capFile:
        yaml.dump(initCapDict, capFile)
    if os.path.exists('%s/%s/currentPositions.ujson' % (Settings.BASE_PATH, dbPath)):
        os.remove('%s/%s/currentPositions.ujson' % (Settings.BASE_PATH, dbPath))


def test_exitTrade():
    CCD, db, posDataMain, ET, _ = before()
    transDB = ET.transDB
    assert len(transDB.all()) == 0
    assert len(db.all()) == 2
    ET.exit(positionDict=posDataMain, currentPrice=9)
    assert len(db.all()) == 1
    assert len(transDB.all()) == 1
    val = transDB.all()[0]
    assert val['closePrice'] == 9
    assert val['percentPnL'] == -0.1
    assert val['realPnL'] == -0.0504
    after()
    CCD.clean()


def test_updateBooks():
    CCD, _, posDataMain, ET, capDict = before()
    ET.exit(positionDict=posDataMain, currentPrice=10)
    ET.updateBooks()
    assert ET.capDict['liquidCurrent'] == 10.499
    assert ET.capDict['paperCurrent'] == 10.699
    after()
    CCD.clean()


if __name__ == '__main__':
    test_paperValue()
    test_exitTrade()
    test_updateBooks()
