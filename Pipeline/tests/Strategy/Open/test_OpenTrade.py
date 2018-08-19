from Pipeline.main.Strategy.Open.OpenTrade import OpenTrade
from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.main.Utils.AddLogger import AddLogger
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from tinydb import TinyDB, Query
import Settings
import yaml


dbPath = '%s/Pipeline/tests/test_DB' % Settings.BASE_PATH
CCD = CreateCleanDir(filePathList=['Pipeline/tests/test_DB/CodeLogs/test_CheapVol',
                                   'Pipeline/tests/test_db/CurrentPositions'])
with open('%s/Configs/testStrat.yml' % dbPath) as file:
    params = yaml.load(file)
baseCapFile = {'initialCapital': 10,'liquidCurrent': 10, 'paperCurrent': 10,'paperPnL': 0, 'percentAllocated': 10}
with open('%s/Capital.yml' % dbPath, 'w') as capFile:
    yaml.dump(baseCapFile, capFile)
CCD.create()
AL = AddLogger('Pipeline/tests/test_DB/CodeLogs/test_CheapVol', stratName='test_CheapVol')
P = Pull('Binance', AL.logger)
db = TinyDB('%s/CurrentPositions/testStrat.ujson' % dbPath)
OT = OpenTrade(configParams=params, compPath=dbPath, Pull=P, db=db)
OT.open('ETHBTC')


def test_open():
    entry = db.search(Query().assetName == 'ETHBTC')
    CCD.clean()
    assert len(entry) == 1
    assert list(entry[0].keys()) == ['assetName', 'openPrice', 'currentPrice', 'periods', 'positionSize', 'TSOpen']


def test_updateBooks():
    OT.updateBooks()
    with open('%s/Capital.yml' % dbPath) as capFile:
        currentCap = yaml.load(capFile)
    assert currentCap['paperCurrent'] == 10 * (1 - 0.05*0.001)
    assert currentCap['liquidCurrent'] == 9.5
    assert currentCap['percentAllocated'] == 0.05
    assert currentCap['paperPnL'] == 1
    with open('%s/Capital.yml' % dbPath, 'w') as capFile:
        yaml.dump(baseCapFile, capFile)


if __name__ == '__main__':
    test_updateBooks()
    test_open()
