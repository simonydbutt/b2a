from Pipeline.main.Strategy.Open.Enter import Enter
from Pipeline.main.Strategy.Open.lib.CheapVol import CheapVol
from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.tests.Strategy.Open.lib.CheapVolTestData import enterData
from Pipeline.main.Utils.AddLogger import AddLogger
from Pipeline.tests.CreateCleanDir import CreateCleanDir
import Settings
import yaml

dbPath = 'Pipeline/tests/test_DB'
CCD = CreateCleanDir(filePathList=['%s/CodeLogs/test_Enter' % dbPath,
                                   '%s/CurrentPositions' % dbPath])
with open('%s/%s/Configs/testStrat.yml' % (Settings.BASE_PATH, dbPath)) as file:
    params = yaml.load(file)


def test_indivEntry():
    CCD.create()
    AL = AddLogger('%s/CodeLogs/test_Enter' % dbPath, stratName='test_Enter')
    E = Enter(stratName='testStrat', dbPath=dbPath, logger=AL.logger, isTest=True)
    P = Pull('Binance', AL.logger)
    CV = CheapVol(params=params, pullData=P, isTest=True)
    assert E.runIndiv(asset='LTCBTC', testData=enterData) == CV.run('LTCBTC', testData=enterData)
    CCD.clean()




if __name__ == '__main__':
    test_indivEntry()