from Pipeline.main.Strategy.Open.lib.CheapVol import CheapVol
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from pymongo import MongoClient
import pandas as pd
import Settings
import logging
import yaml


client = MongoClient('localhost', 27017)
col = client['testCheapVol']['PastPriceAction']
resPath = 'Pipeline/resources/testCheapVol'
CCD = CreateCleanDir([resPath])
params = {
    'assetSelection': {
        'exchangeList': ['Binance']
    },
    'enter': {
        'name': 'CheapVol', 'granularity': 7200, 'periodsVolLong': 5, 'periodsVolShort': 3, 'periodsMA': 5,
        'volCoef': 1, 'bolStd': 1
    }
}
initData = {
    'asset': 'LTC',
    'price': [10, 10, 10, 10, 10],
    'vol': [10, 10, 10, 10, 10]
}
initSingleData = pd.DataFrame([[10, 10], [10, 10], [10, 10], [10, 10], [10, 10]], columns=['close', 'volume'])


def before():
    CCD.create()
    with open('%s/%s/config.yml' % (Settings.BASE_PATH, resPath), 'w') as configFile:
        yaml.dump(params, configFile)


def after():
    client.drop_database('testCheapVol')
    CCD.clean()


def test_initSingle():
    before()
    assert CheapVol(stratName='testCheapVol', assetList=[], isTest=True)._initSingle(
        asset='LTC', exchange='Binance', testData=initSingleData
    )
    logging.debug('Asserting %s == %s' % (col.find_one({'asset': 'LTC'}, {'_id': 0}), initData))
    assert col.find_one({'asset': 'LTC'}, {'_id': 0}) == initData
    after()


def test_initiateCollection():
    before()
    fL = CheapVol(stratName='testCheapVol', isTest=True,
                  assetList=[('LTC', 'Binance'), ('XMR', 'Binance'), ('NotAnAsset', 'Binance')]).initiateCollection()
    logging.debug('Asserting %s == %s' % (fL, ['NotAnAsset']))
    assert fL == ['NotAnAsset']
    logging.debug('Asserting %s == %s' % ([val["asset"] for val in list(col.find())], ['LTC', 'XMR']))
    assert [val["asset"] for val in list(col.find())] == ['LTC', 'XMR']
    after()


def test_before():
    before()
    cV = CheapVol(stratName='testCheapVol', isTest=True, assetList=[('LTC', 'Binance'), ('XMR', 'Binance')])
    cV.initiateCollection()
    newData = {'LTC': {'price': 10, 'vol': 5}, 'XMR': {'price': 20, 'vol': 10}}
    cV.before(testData=newData)
    logging.debug('Asserting %s == %s' % ([val["asset"] for val in list(col.find())], ['LTC', 'XMR']))
    assert {val['asset']: {'price': val['price'][-1], 'vol': val['vol'][-1]} for val in list(col.find())} == newData
    ppaData = col.find_one()
    assert len(ppaData['price']) == len(ppaData['vol']) == 5
    after()


def test_run():
    before()
    CV = CheapVol(stratName='testCheapVol', assetList=['LTC', 'XMR'], isTest=True)
    col.insert_many([{'asset': 'enter', 'price': [10, 10, 10, 10, 0.4], 'vol': [10, 10, 10, 10, 20]},
                     {'asset': 'volTooSmall', 'price': [10, 10, 10, 10, 10], 'vol': [20, 30, 10, 10, 20]},
                     {'asset': 'priceTooLarge', 'price': [10, 10, 10, 10, 20], 'vol': [10, 10, 10, 10, 10]}])
    # Will enter position
    assert CV.run(asset='enter')
    # Volume too small to enter
    assert not CV.run(asset='volTooSmall')
    # Price too large to enter
    assert not CV.run(asset='priceTooLarge')
    after()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_initSingle()
    test_initiateCollection()
    test_before()
    test_run()