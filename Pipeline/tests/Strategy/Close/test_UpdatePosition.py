from Pipeline.main.Strategy.Close.UpdatePosition import UpdatePosition
from pymongo import MongoClient
import Settings
import logging


def test_update():
    client = MongoClient('localhost', 27017)
    client.drop_database('testUpdatePos')
    col = client['testUpdatePos']['currentPositions']
    UP = UpdatePosition(stratName='testUpdatePos')
    positionDict={
        'currentPrice': 11,
        'openPrice': 10,
        'assetName': 'LTCBTC',
        'paperSize': 110,
        'periods': 2,
        'positionSize': 100,
    }
    col.insert_one(positionDict)
    UP.update(positionDict=positionDict, currentPrice=10)
    assert col.count() == 1
    newVal = col.find_one()
    assert newVal['periods'] == 3
    assert newVal['currentPrice'] == 10
    assert newVal['paperSize'] == 100
    UP.update(positionDict=positionDict, currentPrice=2)
    assert col.find_one()['paperSize'] == 20
    client.drop_database('testUpdatePos')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_update()
