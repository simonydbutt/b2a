from Pipeline.main.Strategy.Open.Enter import Enter
from Pipeline.main.Strategy.Open.lib.CheapVol import CheapVol
from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.tests.Strategy.Open.lib.CheapVolTestData import enterData
from Pipeline.tests.CreateCleanDir import CreateCleanDir
import logging
import Settings
import yaml

"""
    *TODO properly test this one --> test_run!!!!!!!
"""


def before():
    dbPath = 'Pipeline/resources/testEnterStrat'
    CCD = CreateCleanDir(filePathList=[dbPath])
    CCD.create()
    configParams = {
        'enter': {'bolStd': 2, 'granularity': 43200, 'name': 'CheapVol', 'periodsMA': 5, 'periodsVolLong': 5,
                  'periodsVolShort': 5, 'volCoef': 1.5},
        'stratName': 'testStrat',
        'logging': {'console': 10, 'file': 20}
    }
    with open('%s/%s/config.yml' % (Settings.BASE_PATH, dbPath), 'w') as configFile:
        yaml.dump(configParams, configFile)
    capitalParams = {'initialCapital': 10, 'liquidCurrent': 10, 'paperCurrent': 10, 'paperPnL': 0, 'percentAllocated': 10}
    with open('%s/%s/capital.yml' % (Settings.BASE_PATH, dbPath), 'w') as capFile:
        yaml.dump(capitalParams, capFile)
    return CCD, configParams


def test_indivEntry():
    CCD, params= before()
    E = Enter(stratName='testEnterStrat', isTest=True)
    P = Pull()
    CV = CheapVol(stratName='testEnterStrat', isTest=True)
    assert E.runIndiv(asset='LTCBTC', Pull=P, testData=enterData) == CV.run('LTCBTC', Pull=P, testData=enterData)
    CCD.clean()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_indivEntry()