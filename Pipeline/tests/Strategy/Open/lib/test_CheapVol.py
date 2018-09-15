from Pipeline.main.Strategy.Open.lib.CheapVol import CheapVol
from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.tests.Strategy.Open.lib.CheapVolTestData import *
from Pipeline.tests.CreateCleanDir import CreateCleanDir
import Settings
import logging
import yaml


resPath = 'Pipeline/resources/testCheapVol'
CCD = CreateCleanDir([resPath])
params = {'enter': {
    'name': 'CheapVol', 'granularity': 7200, 'periodsVolLong': 5, 'periodsVolShort': 3, 'periodsMA': 5,
    'volCoef': 1, 'bolStd': 1
}}


def test_CheapVol():
    CCD.create()
    with open('%s/%s/config.yml' % (Settings.BASE_PATH, resPath), 'w') as configFile:
        yaml.dump(params, configFile)
    P = Pull()
    CV = CheapVol(stratName='testCheapVol', isTest=True)
    # Will enter position
    assert CV.run(asset='LTCBTC', exchange='Binance', testData=enterData, Pull=P)
    # Volume too small to enter
    assert not CV.run(asset='LTCBTC', exchange='Binance', testData=volSmallData, Pull=P)
    # Price too large to enter
    assert not CV.run(asset='LTCBTC', exchange='Binance', testData=closeLargeData, Pull=P)
    CCD.clean()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_CheapVol()