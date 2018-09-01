from Pipeline.main.Strategy.Close.UpdatePosition import UpdatePosition
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from tinydb import TinyDB, Query
import Settings


def before():
    dbPath = 'Pipeline/tests/test_DB'
    CCD = CreateCleanDir(filePathList=['%s/CurrentPositions' % dbPath])
    CCD.create()
    db = TinyDB('%s/%s/CurrentPositions/test.ujson' % (Settings.BASE_PATH, dbPath))
    posDataMain = {'assetName': 'ADABTC', 'openPrice': 0.0000158, 'currentPrice': 0.0000158, 'periods': 2,
                   'positionSize': 0.4995, 'paperSize': 0.4995, 'TSOpen': 1534711395, 'hitPrice': 11, 'sellPrice': 9}
    db.insert(posDataMain)
    CCD.create()
    return CCD, db, posDataMain


def test_update():
    CCD, db, posDataMain = before()
    UpdatePosition(db).update(positionDict=posDataMain, currentPrice=10)
    val = db.search(Query().assetName == 'ADABTC')[0]
    assert val['currentPrice'] == 10
    assert val['periods'] == 3
    CCD.clean()


if __name__ == '__main__':
    test_update()
