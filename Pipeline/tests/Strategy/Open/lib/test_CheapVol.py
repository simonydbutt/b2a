from Pipeline.main.Strategy.Open.lib.CheapVol import CheapVol
from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.tests.Strategy.Open.lib.CheapVolTestData import *
from Pipeline.main.Utils.AddLogger import AddLogger
from Pipeline.tests.CreateCleanDir import CreateCleanDir
import Settings
import yaml


CCD = CreateCleanDir(filePathList=['Pipeline/tests/test_DB/CodeLogs/test_CheapVol'])
with open('%s/Pipeline/tests/test_DB/Configs/testStrat.yml' % Settings.BASE_PATH) as file:
    params = yaml.load(file)


def test_CheapVol():
    CCD.create()
    AL = AddLogger('Pipeline/tests/test_DB/CodeLogs/test_CheapVol', stratName='test_CheapVol')
    P = Pull('Binance', AL.logger)
    CV = CheapVol(params=params, isTest=True, pullData=P)
    # Will enter position
    assert CV.run(asset='LTCBTC', testData=enterData)
    # Volume too small to enter
    assert not CV.run(asset='LTCBTC', testData=volSmallData)
    # Price too large to enter
    assert not CV.run(asset='LTCBTC', testData=closeLargeData)
    CCD.clean()


if __name__ == '__main__':
    test_CheapVol()