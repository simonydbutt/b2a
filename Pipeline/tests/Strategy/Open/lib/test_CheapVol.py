from Pipeline.main.Strategy.Open.lib.CheapVol import CheapVol
from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.tests.Strategy.Open.lib.CheapVolTestData import *
import logging


params = {'enter': {
    'name': 'CheapVol', 'granularity': 7200, 'periodsVolLong': 5, 'periodsVolShort': 3, 'periodsMA': 5,
    'volCoef': 1, 'bolStd': 1
}}


def test_CheapVol():
    P = Pull('Binance')
    CV = CheapVol(params=params, isTest=True)
    # Will enter position
    assert CV.run(asset='LTCBTC', testData=enterData, Pull=P)
    # Volume too small to enter
    assert not CV.run(asset='LTCBTC', testData=volSmallData, Pull=P)
    # Price too large to enter
    assert not CV.run(asset='LTCBTC', testData=closeLargeData, Pull=P)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_CheapVol()