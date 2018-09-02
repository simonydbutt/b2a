from Pipeline.main.Strategy.Open.lib.CheapVol import CheapVol
from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.tests.Strategy.Open.lib.CheapVolTestData import *
from Pipeline.main.Utils.AddLogger import AddLogger
from Pipeline.tests.CreateCleanDir import CreateCleanDir
import Settings
import yaml

dbPath = 'Pipeline/DB/test'
CCD = CreateCleanDir(filePathList=['%s/CodeLogs' % dbPath])
with open('%s/%s/config.yml' % (Settings.BASE_PATH, dbPath)) as file:
    params = yaml.load(file)


def test_CheapVol():
    CCD.create()
    AL = AddLogger(dirPath='%s/CodeLogs' % dbPath, stratName='testCheapVol')
    P = Pull('Binance', AL.logger)
    CV = CheapVol(params=params, isTest=True)
    # Will enter position
    assert CV.run(asset='LTCBTC', testData=enterData, Pull=P)
    # Volume too small to enter
    assert not CV.run(asset='LTCBTC', testData=volSmallData, Pull=P)
    # Price too large to enter
    assert not CV.run(asset='LTCBTC', testData=closeLargeData, Pull=P)
    CCD.clean()


if __name__ == '__main__':
    test_CheapVol()