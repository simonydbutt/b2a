from Pipeline.main.Strategy.Close.ExitTrade import ExitTrade
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from tinydb import TinyDB
import Settings
import yaml
import os


dbPath = 'Pipeline/DB/test'
compPath = '%s/%s' % (Settings.BASE_PATH, dbPath)


def before():
    if os.path.exists('%s/currentPositions.ujson' % compPath):
        os.remove('%s/currentPositions.ujson' % compPath)
    db = TinyDB('%s/currentPositions.ujson' % compPath)
    posDataMain = {'assetName': 'ADABTC', 'openPrice': 10, 'currentPrice': 9, 'periods': 2, 'exchange': 'Binance',
                   'positionSize': 0.4995, 'paperSize': 0.4995, 'TSOpen': 1534711395, 'hitPrice': 11, 'sellPrice': 9}
    posDataSub = {'assetName': 'TESTBTC', 'openPrice': 0.0000158, 'currentPrice': 0.0000158, 'periods': 2,
                  'positionSize': 0.4995, 'paperSize': 0.2, 'TSOpen': 1534711395, 'hitPrice': 11, 'sellPrice': 9,
                  'exchange': 'Binance'}
    db.insert(posDataMain)
    db.insert(posDataSub)
    initCapDict = {
        'initialCapital': 10, 'liquidCurrent': 10, 'paperCurrent': 10,
        'paperPnL': 0, 'percentAllocated': 0
    }
    with open('%s/capital.yml' % compPath, 'w') as capFile:
        yaml.dump(initCapDict, capFile)
    ET = ExitTrade(compPath='%s/%s' % (Settings.BASE_PATH, dbPath), db=db)
    return db, posDataMain, ET, initCapDict


def test_paperValue():
    db, _, ET, _ = before()
    assert ET.paperValue() == 0.6995
    after()


def after():
    initCapDict = {
        'initialCapital': 10, 'liquidCurrent': 10, 'paperCurrent': 10,
        'paperPnL': 0, 'percentAllocated': 0
    }
    for file in ('currentPositions.ujson', 'transactionLogs.ujson', 'capital.yml'):
        if os.path.exists('%s/%s' % (compPath, file)):
            os.remove('%s/%s' % (compPath, file))

def test_exitTrade():
    db, posDataMain, ET, _ = before()
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


def test_updateBooks():
    _, posDataMain, ET, capDict = before()
    ET.exit(positionDict=posDataMain, currentPrice=10)
    ET.updateBooks()
    assert ET.capDict['liquidCurrent'] == 10.499
    assert ET.capDict['paperCurrent'] == 10.699
    after()


if __name__ == '__main__':
    test_paperValue()
    test_exitTrade()
    test_updateBooks()
