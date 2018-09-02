from Pipeline.main.Strategy.Open.Enter import Enter
from Pipeline.main.Strategy.Open.lib.CheapVol import CheapVol
from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.tests.Strategy.Open.lib.CheapVolTestData import enterData
from Pipeline.main.Utils.AddLogger import AddLogger
from Pipeline.tests.CreateCleanDir import CreateCleanDir
import Settings
import yaml
import os


def before():
    dbPath = 'Pipeline/DB/test'
    CCD = CreateCleanDir(filePathList=['%s/test_Enter' % dbPath, '%s/test_Enter/CodeLogs' % dbPath])
    CCD.create()
    with open('%s/%s/config.yml' % (Settings.BASE_PATH, dbPath)) as file:
        params = yaml.load(file)
    with open('%s/%s/test_Enter/config.yml' % (Settings.BASE_PATH, dbPath), 'w') as configFile:
        yaml.dump(params, configFile)
    return CCD, params, dbPath


def test_indivEntry():
    CCD, params, dbPath = before()
    AL = AddLogger(db='test', stratName='test_Enter')
    E = Enter(db='test', stratName='test_Enter', isTest=True)
    P = Pull('Binance', AL.logger)
    CV = CheapVol(params=params, isTest=True)
    assert E.runIndiv(asset='LTCBTC', Pull=P, testData=enterData) == CV.run('LTCBTC', Pull=P, testData=enterData)
    CCD.clean()


if __name__ == '__main__':
    test_indivEntry()