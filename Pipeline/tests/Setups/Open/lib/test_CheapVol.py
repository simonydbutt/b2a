from Pipeline.main.Setups.Open.lib.CheapVol import CheapVol
from Pipeline.tests.Setups.Open.lib.CheapVolTestData import *
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
    CV = CheapVol(params=params, logger=AL.logger, isTest=True)
    # Will enter position
    assert CV.run(asset='LTCBTC', testData=enterData)
    # Volume too small to enter
    assert not CV.run(asset='LTCBTC', testData=volSmallData)
    # Price too large to enter
    assert not CV.run(asset='LTCBTC', testData=closeLargeData)
    CCD.clean()


if __name__ == '__main__':
    test_CheapVol()