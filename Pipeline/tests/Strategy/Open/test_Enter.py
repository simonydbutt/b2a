from Pipeline.main.Strategy.Open.Enter import Enter
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from pymongo import MongoClient
import logging
import Settings
import yaml


client = MongoClient('localhost', 27017)
col = client['testEnter']['currentPositions']
resPath = 'Pipeline/resources/testEnter'
CCD = CreateCleanDir([resPath])
params = {
    'assetSelection': {
        'exchangeList': ['Binance', 'Hadax']
    },
    'enter': {
        'name': 'TestingStrat'
    }
}
assetList = [('XMR', 'Binance'), ('LTC', 'Hadax'), ('ETH', 'Binance')]


def before():
    CCD.create()
    with open('%s/%s/config.yml' % (Settings.BASE_PATH, resPath), 'w') as configFile:
        yaml.dump(params, configFile)
    col.insert_one({'assetName': 'XMRBTC'})


def after():
    client.drop_database('testEnter')
    CCD.clean()


def test_run():
    before()
    oL = Enter(stratName='testEnter', isTest=True, testAssets=assetList).run()
    assert oL == ['ETH']
    after()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_run()