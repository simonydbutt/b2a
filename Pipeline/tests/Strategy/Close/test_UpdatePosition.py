from Pipeline.main.Strategy.Close.UpdatePosition import UpdatePosition
from tinydb import TinyDB
import Settings
import os


def test_update():
    dbPath = '%s/Pipeline/DB/test' % Settings.BASE_PATH
    db = TinyDB('%s/currentPositions.ujson' % dbPath)
    positionDict={
        'currentPrice': 11,
        'openPrice': 10,
        'assetName': 'LTCBTC',
        'paperSize': 110,
        'periods': 2,
        'positionSize': 100
    }
    db.insert(positionDict)
    UP = UpdatePosition(db=db)
    UP.update(positionDict=positionDict, currentPrice=10)
    assert len(db.all()) == 1
    newVal = db.all()[0]
    assert newVal['periods'] == 3
    assert newVal['currentPrice'] == 10
    assert newVal['paperSize'] == 100
    UP.update(positionDict=positionDict, currentPrice=2)
    assert db.all()[0]['paperSize'] == 20
    os.remove('%s/currentPositions.ujson' % dbPath)


if __name__ == '__main__':
    test_update()
