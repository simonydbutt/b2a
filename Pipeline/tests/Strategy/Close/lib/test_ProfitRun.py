from Pipeline.main.Strategy.Close.lib.ProfitRun import ProfitRun
from Pipeline.main.Utils.AddLogger import AddLogger
from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from tinydb import TinyDB
import Settings
import yaml


def before():
    dbPath = 'Pipeline/tests/test_DB'
    CCD = CreateCleanDir(filePathList=['%s/CodeLogs/testProfitRun' % dbPath,
                                       '%s/CurrentPositions' % dbPath])
    CCD.create()
    AL = AddLogger(dirPath='Pipeline/tests/test_DB/CodeLogs/testProfitRun', stratName='testProfitRun')
    P = Pull('Binance', AL.logger)
    db = TinyDB('%s/%s/CurrentPositions/test.ujson' % (Settings.BASE_PATH, dbPath))
    posData = {'assetName':'ADABTC','openPrice':0.0000158,'currentPrice':0.0000158,'periods':0,
               'positionSize':0.4995, 'paperSize': 0.4995, 'TSOpen':1534711395}
    db.insert(posData)
    with open('%s/Pipeline/tests/test_DB/Configs/testStrat.yml' % Settings.BASE_PATH) as file:
        params = yaml.load(file)
    PR = ProfitRun(pullData=P, configParams=params, db=db)
    return PR, db, CCD


def test_updatePostition():
    PR, db, CCD = before()
    CCD.clean()


if __name__ == '__main__':
    test_updatePostition()