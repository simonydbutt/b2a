from Pipeline.main.Deploy.Build import Build
import Settings
import shutil
import os


path = '%s/Pipeline/DB/test/testStrat' % Settings.BASE_PATH


def beforeAfter():
    if os.path.exists(path):
        shutil.rmtree(path)


def test_buildStrat():
    Build(stratName='testStrat', dbName='test', initialCapital=10, positionSizeParams={'name': 'Basic', 'percent': 0.05},
          assetSelectionParams={'name': 'all', 'exchangeList': ['Binance'], 'baseAsset': 'BTC'},
          enterParams={'name': 'CheapVol', 'granularity': 43200, 'periodsVolLong': 100, 'periodsVolShort': 5,
                       'periodsMA': 100, 'volCoef': 1.5, 'bolStd': 2},
          exitParams={'name': 'ProfitRun', 'granularity': 7200, 'periodsVolLong': 50, 'periodsVolShort': 5,
                      'periodsMA': 50, 'volCoef': 1, 'bolStd': 2})
    for file in ('CodeLogs', 'TransactionLogs', 'config.yml', 'capital.yml'):
        assert os.path.exists('%s/%s' % (path, file))
    beforeAfter()


if __name__ == '__main__':
    test_buildStrat()
