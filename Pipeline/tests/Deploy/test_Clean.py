from Pipeline.main.Deploy.Clean import Clean
from Pipeline.main.Deploy.Build import Build
from tinydb import TinyDB
import Settings
import shutil
import time
import yaml
import os


path = '%s/Pipeline/DB/test' % Settings.BASE_PATH
stratPath = '%s/testStrat' % path
archivePath = '%s/archive' % path


def before():
    if os.path.exists(stratPath):
        shutil.rmtree(stratPath)
    if os.path.exists(archivePath):
        shutil.rmtree(archivePath)
    Build(stratName='testStrat', dbName='test', initialCapital=10, positionSizeParams={'name': 'Basic', 'percent': 0.05},
          assetSelectionParams={'name': 'all', 'exchangeList': ['Binance'], 'baseAsset': 'BTC'},
          enterParams={'name': 'CheapVol', 'granularity': 43200, 'periodsVolLong': 100, 'periodsVolShort': 5,
                       'periodsMA': 100, 'volCoef': 1.5, 'bolStd': 2},
          exitParams={'name': 'ProfitRun', 'granularity': 7200, 'periodsVolLong': 50, 'periodsVolShort': 5,
                      'periodsMA': 50, 'volCoef': 1, 'bolStd': 2})
    if not os.path.exists(archivePath):
        os.mkdir(archivePath)


def after():
    if os.path.exists(stratPath):
        shutil.rmtree(stratPath)
    if os.path.exists(archivePath):
        shutil.rmtree(archivePath)


def test_cleanStrat():
    before()
    Clean(db='test', stratName='testStrat').cleanStrat()
    assert not os.path.exists(stratPath)
    after()


def test_resetStrat():
    before()
    with open('%s/capital.yml' % stratPath) as capFile:
        cap = yaml.load(capFile)
        cap['liquidCurrent'] = 0
    with open('%s/capital.yml' % stratPath, 'w') as capFile:
        yaml.dump(data=cap, stream=capFile)
    db = TinyDB('%s/currentPositions.ujson' % stratPath)

    db.insert({'a':1})
    open('%s/CodeLogs/testLog' % (stratPath), 'a').close()
    Clean('test', 'testStrat').resetStrat()
    assert len(TinyDB('%s/currentPositions.ujson' % stratPath).all()) == 0
    assert len(TinyDB('%s/transactionLogs.ujson' % stratPath).all()) == 0
    assert len(os.listdir('%s/Codelogs' % stratPath)) == 0
    with open('%s/capital.yml' % stratPath, 'r+') as capFile:
        cap = yaml.load(capFile)
    assert cap == {'initialCapital': 10, 'liquidCurrent': 10, 'paperCurrent': 10, 'paperPnL': 0, 'percentAllocated': 0}
    after()


if __name__ == '__main__':
    test_cleanStrat()
    test_resetStrat()