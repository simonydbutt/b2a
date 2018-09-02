from Pipeline.main.Monitor.StatsUpdate import StatsUpdate
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from tinydb import TinyDB
import Settings
import yaml


def before():
    dbPath = 'Pipeline/DB/statTest'
    compPath = '%s/%s' % (Settings.BASE_PATH, dbPath)
    CCD = CreateCleanDir([dbPath, '%s/strat1' % dbPath, '%s/strat2' % dbPath])
    CCD.clean()
    CCD.create()
    for strat in ('strat1', 'strat2'):
        cDB = TinyDB('%s/%s/currentPositions.ujson' % (compPath, strat))
        cDB.insert({'assetName': 'LTCBTC'})
        tDB = TinyDB('%s/%s/transactionLogs.ujson' % (compPath, strat))
        for i in [{'a': 1}, {'b': 2}, {'c': 2}]:
            tDB.insert(i)
        capitalDict = {'initialCapital': 10, 'liquidCurrent': 9, 'paperCurrent': 11,
                       'paperPnL': 0.1, 'percentAllocated': 0.1}
        with open('%s/%s/capital.yml' % (compPath, strat), 'w') as capFile:
            yaml.dump(capitalDict, capFile)
    return CCD, dbPath


def test_indivStats():
    CCD, dbPath = before()
    SU = StatsUpdate(dbPath)
    stats = SU.indivStats('strat1')
    assert stats['initialCapital'] == 10
    assert stats['numberOpen'] == 1
    assert stats['numberTransactions'] == 3
    assert stats['openList'] == ['LTCBTC']
    assert stats['paperAvgPnL'] == 0.025
    CCD.clean()


def test_compStats():
    CCD, dbPath = before()
    SU = StatsUpdate(dbPath)
    statDict = SU.compStats()
    assert len(list(statDict)) == 3
    totDict = statDict['total']
    assert totDict['numberOpen'] == 2
    assert totDict['initialCapital'] == 20
    assert totDict['liquidCurrent'] == 18
    assert totDict['paperCurrent'] == 22
    assert totDict['percentAllocated'] == 18
    CCD.clean()


if __name__ == '__main__':
    test_indivStats()
    test_compStats()