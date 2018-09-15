from Pipeline.main.Strategy.Close.lib.ProfitRun import ProfitRun
from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from pymongo import MongoClient
import pandas as pd
import Settings
import logging
import yaml


resPath = 'Pipeline/resources/testProfitRun'
CCD = CreateCleanDir([resPath])
client = MongoClient('localhost', 27017)
col = client['testProfitRun']['currentPositions']


def before():
    P = Pull()
    CCD.create()
    posDataInit = {'assetName': 'ADABTC', 'openPrice': 0.0000158, 'currentPrice': 9, 'periods': 0,
                   'positionSize': 0.4995, 'paperSize': 0.4995, 'TSOpen': 1534711395, 'exchange': 'Binance'}
    posDataMain = {'assetName': 'ETHBTC', 'openPrice': 0.0000158, 'currentPrice': 10, 'periods': 0, 'hitPrice': 11,
                   'positionSize': 0.4995, 'paperSize': 0.4995, 'TSOpen': 1534711395, 'sellPrice': 9, 'exchange': 'Binance'}
    posDataPeriods = {'assetName': 'LTCBTC', 'openPrice': 0.0000158, 'currentPrice': 0.0000158, 'periods': 6, 'sellPrice': 9,
                      'positionSize': 0.4995, 'paperSize': 0.4995, 'TSOpen': 1534711395, 'hitPrice': 11, 'exchange': 'Binance'}
    updatePosData = pd.DataFrame(
        data=[
            [10], [9], [8], [11], [7]
        ], columns=['close']
    )
    col.insert_many([posDataMain, posDataInit, posDataPeriods])
    params = {'exit': {
        'bolStd': 2, 'granularity': 7200, 'name': 'ProfitRun', 'maPeriods': 5, 'closePeriods': 5,
        'stdDict': {'up': 1, 'down': 0.5}}
    }
    with open('%s/%s/config.yml' % (Settings.BASE_PATH, resPath), 'w') as configFile:
        yaml.dump(params, configFile)
    PR = ProfitRun('testProfitRun', isTest=True)
    return PR, P, {'main': posDataMain, 'init': posDataInit, 'periods': posDataPeriods}, updatePosData


def after():
    client.drop_database('testProfitRun')
    CCD.clean()


def test_updatePostition():
    PR, P, posDict, updatePosData = before()
    PR.updatePosition(positionData=posDict['init'], testData=updatePosData, Pull=P)
    doc = col.find_one({'assetName': 'ADABTC'})
    assert round(doc['hitPrice'], 4) == 10.4142
    assert round(doc['sellPrice'], 4) == 8.2929
    after()


def test_profitRun():
    PR, P, posDict, updatePosData = before()
    # update & initial
    assert not PR.run(positionData=posDict['init'], testPrice=10, testData=updatePosData, Pull=P)[0]
    # update & norm
    assert not PR.run(positionData=posDict['main'], testPrice=12, testData=updatePosData, Pull=P)[0]
    # in normal range
    assert not PR.run(positionData=posDict['main'], testPrice=11, Pull=P)[0]
    # close as too small
    assert PR.run(positionData=posDict['main'], testPrice=8.9, Pull=P)[0]
    # close as periods out
    assert PR.run(positionData=posDict['periods'], testPrice=10, Pull=P)[0]
    after()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_updatePostition()
    test_profitRun()
