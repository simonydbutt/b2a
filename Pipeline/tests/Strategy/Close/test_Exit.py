from Pipeline.main.Strategy.Close.lib.ProfitRun import ProfitRun
from Pipeline.main.Strategy.Close.Exit import Exit
from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from pymongo import MongoClient
import Settings
import logging
import yaml


resPath = 'Pipeline/resources/testExit'
CCD = CreateCleanDir(filePathList=[resPath])
client = MongoClient('localhost', 27017)
col = client['testExit']['currentPositions']
posDataMain = {'assetName': 'ADABTC', 'openPrice': 0.0000158, 'currentPrice': 0.0000158, 'periods': 0, 'sellPrice': 9,
               'positionSize': 0.4995, 'paperSize': 0.4995, 'TSOpen': 1534711395, 'hitPrice': 11, 'exchange': 'Binance'}


def before():
    CCD.create()
    col.insert_one(posDataMain)
    params = {'isLive': False,
              'exit': {'bolStd': 2, 'granularity': 7200, 'name': 'ProfitRun', 'maPeriods': 5, 'closePeriods': 5,
                       'stdDict': {'up': 1, 'down': 0.5}, 'exchange': 'Binance'}}
    with open('%s/%s/config.yml' % (Settings.BASE_PATH, resPath), 'w') as configFile:
        yaml.dump(params, configFile)
    PR = ProfitRun(stratName='testExit', isTest=True)
    E = Exit(stratName='testExit', isTest=True)
    P = Pull()
    return PR, E, P


def after():
    client.drop_database('testExit')
    CCD.clean()


def test_runIndiv():
    PR, E, P = before()
    assert PR.run(positionData=posDataMain, testPrice=10, Pull=P) == E.runIndiv(positionData=posDataMain, testPrice=10, Pull=P)
    after()


# *TODO create proper test for Exit.run()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_runIndiv()
