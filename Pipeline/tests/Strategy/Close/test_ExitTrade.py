from Pipeline.main.Strategy.Close.ExitTrade import ExitTrade
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from pymongo import MongoClient
import Settings
import logging
import yaml


resPath = 'Pipeline/resources/testExitTrade'
CCD = CreateCleanDir([resPath])
posDataMain = {'assetName': 'ADABTC', 'openPrice': 10, 'currentPrice': 9, 'periods': 2, 'exchange': 'Binance',
               'positionSize': 0.4995, 'paperSize': 0.4995, 'TSOpen': 1534711395, 'hitPrice': 11, 'sellPrice': 9}
posDataSub = {'assetName': 'TESTBTC', 'openPrice': 0.0000158, 'currentPrice': 0.0000158, 'periods': 2,
              'positionSize': 0.4995, 'paperSize': 0.2, 'TSOpen': 1534711395, 'hitPrice': 11, 'sellPrice': 9,
              'exchange': 'Binance'}
client = MongoClient('localhost', 27017)
currentCol = client['testExitTrade']['currentPositions']
transCol = client['testExitTrade']['transactionLogs']


def before():
    CCD.create()
    client.drop_database('testExitTrade')
    currentCol.insert_many([posDataMain, posDataSub])
    initCapDict = {
        'initialCapital': 10, 'liquidCurrent': 10, 'paperCurrent': 10,
        'paperPnL': 0, 'percentAllocated': 0
    }
    with open('%s/%s/capital.yml' % (Settings.BASE_PATH, resPath), 'w') as capFile:
        yaml.dump(initCapDict, capFile)
    ET = ExitTrade(stratName='testExitTrade')
    ET.initBooks()
    return ET


def test_paperValue():
    ET = before()
    assert ET.paperValue() == 0.6995
    after()


def after():
    client.drop_database('testExitTrade')
    CCD.clean()


def test_exitTrade():
    ET = before()
    assert transCol.count() == 0
    assert currentCol.count() == 2
    ET.exit(positionDict=posDataMain, currentPrice=9)
    assert currentCol.count() == 1
    assert transCol.count() == 1
    val = transCol.find_one()
    assert val['closePrice'] == 9
    assert val['percentPnL'] == -0.1
    assert val['realPnL'] == -0.0504
    after()


def test_closeOutBooks():
    ET = before()
    ET.exit(positionDict=posDataMain, currentPrice=10)
    ET.closeOutBooks()
    assert ET.capDict['liquidCurrent'] == 10.499
    assert ET.capDict['paperCurrent'] == 10.699
    after()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_paperValue()
    test_exitTrade()
    test_closeOutBooks()
