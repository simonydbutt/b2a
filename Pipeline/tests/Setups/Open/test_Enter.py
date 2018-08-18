from Pipeline.main.Setups.Open.Enter import Enter
from Pipeline.main.Setups.Open.lib.CheapVol import CheapVol
from Pipeline.tests.Setups.Open.lib.CheapVolTestData import enterData
from Pipeline.main.Utils.AddLogger import AddLogger
from Pipeline.tests.CreateCleanDir import CreateCleanDir
import Settings
import yaml


CCD = CreateCleanDir(filePathList=['Pipeline/tests/test_DB/CodeLogs/test_Enter'])
with open('%s/Pipeline/tests/test_DB/Configs/testStrat.yml' % Settings.BASE_PATH) as file:
    params = yaml.load(file)


def test_Enter():
    CCD.create()
    AL = AddLogger('Pipeline/tests/test_DB/CodeLogs/test_Enter', stratName='test_Enter')
    E = Enter(stratName='testStrat', stratPath='Pipeline/tests/test_DB/Configs', logger=AL.logger, isTest=True)
    CV = CheapVol(params=params, logger=AL.logger, isTest=True)
    assert E.run(asset='LTCBTC', testData=enterData) == CV.run('LTCBTC', testData=enterData)
    CCD.clean()


if __name__ == '__main__':
    test_Enter()