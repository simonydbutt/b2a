from Pipeline.main.Strategy.Close.ExitTrade import ExitTrade
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from tinydb import TinyDB
import Settings
import yaml


def before():
    dbPath = 'Pipeline/tests/test_DB'
    CCD = CreateCleanDir(filePathList=['%s/CurrentPositions' % dbPath,
                                       '%s/TransactionLogs' % dbPath])
    CCD.clean()
    CCD.create()
    db = TinyDB('%s/%s/CurrentPositions/test.ujson' % (Settings.BASE_PATH, dbPath))
    posDataMain = {'assetName': 'ADABTC', 'openPrice': 10, 'currentPrice': 9, 'periods': 2,
                   'positionSize': 0.4995, 'paperSize': 0.4995, 'TSOpen': 1534711395, 'hitPrice': 11, 'sellPrice': 9}
    posDataSub = {'assetName': 'TESTBTC', 'openPrice': 0.0000158, 'currentPrice': 0.0000158, 'periods': 2,
                   'positionSize': 0.4995, 'paperSize': 0.2, 'TSOpen': 1534711395, 'hitPrice': 11, 'sellPrice': 9}
    db.insert(posDataMain)
    db.insert(posDataSub)
    ET = ExitTrade(compPath='%s/%s' % (Settings.BASE_PATH, dbPath), db=db, stratName='testStrat', fees=0.001)
    with open('%s/%s/Capital.yml' % (Settings.BASE_PATH, dbPath)) as capFile:
        capDict = yaml.load(capFile)
    return CCD, db, posDataMain, ET, capDict


def after(capDict):
    dbPath = 'Pipeline/tests/test_DB'
    with open('%s/%s/Capital.yml' % (Settings.BASE_PATH, dbPath), 'w') as capFile:
        yaml.dump(capDict, capFile)


def test_paperValue():
    CCD, db, _, ET, _ = before()
    assert ET.paperValue() == 0.6995
    CCD.clean()


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
    CCD.clean()


def test_updateBooks():
    CCD, _, posDataMain, ET, capDict = before()
    ET.exit(positionDict=posDataMain, currentPrice=10)
    ET.updateBooks()
    assert ET.capDict['liquidCurrent'] == 10.499
    assert ET.capDict['paperCurrent'] == 10.699
    after(capDict)
    CCD.clean()


if __name__ == '__main__':
    test_paperValue()
    test_exitTrade()
    test_updateBooks()
