from Pipeline.main.Strategy.Open.OpenTrade import OpenTrade
from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.main.Utils.AddLogger import AddLogger
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from tinydb import TinyDB, Query
import Settings
import yaml
import os


dbPath = 'Pipeline/DB/test'
compPath = '%s/%s' % (Settings.BASE_PATH, dbPath)


def Enter():
    CCD = CreateCleanDir(filePathList=['%s/CodeLogs' % dbPath])
    with open('%s/config.yml' % compPath) as file:
        params = yaml.load(file)
    baseCapFile = {'initialCapital': 10,'liquidCurrent': 10, 'paperCurrent': 10,'paperPnL': 0, 'percentAllocated': 10}
    with open('%s/Capital.yml' % compPath, 'w') as capFile:
        yaml.dump(baseCapFile, capFile)
    CCD.create()
    AL = AddLogger(dirPath='%s/CodeLogs' % dbPath, stratName='test_CheapVol')
    P = Pull('Binance', AL.logger)
    db = TinyDB('%s/currentPositions.ujson' % compPath)
    OT = OpenTrade(configParams=params, compPath=compPath, db=db)
    OT.open(assetVals=('ETHBTC', 'Binance'), Pull=P)
    return baseCapFile, db, CCD, compPath, OT


def after():
    os.remove('%s/currentPositions.ujson' % compPath)


def test_open():
    baseCapFile, db, CCD, dbPath, OT = Enter()
    entry = db.search(Query().assetName == 'ETHBTC')
    assert len(entry) == 1
    assert list(entry[0].keys()) == ['assetName', 'openPrice', 'currentPrice', 'periods',
                                     'positionSize', 'paperSize', 'TSOpen', 'exchange']
    CCD.clean()
    after()


def test_updateBooks():
    baseCapFile, db, CCD, dbPath, OT = Enter()
    OT.updateBooks()
    with open('%s/Capital.yml' % dbPath) as capFile:
        currentCap = yaml.load(capFile)
    assert currentCap['paperCurrent'] == 10 * (1 - 0.05*0.001)
    assert currentCap['liquidCurrent'] == 9.5
    assert currentCap['percentAllocated'] == 0.05
    assert currentCap['paperPnL'] == 1
    with open('%s/Capital.yml' % dbPath, 'w') as capFile:
        yaml.dump(baseCapFile, capFile)
    CCD.clean()
    after()


if __name__ == '__main__':
    test_updateBooks()
    test_open()
