from Pipeline.main.Audit.DailyCapital import DailyCapital
import os
import Settings


dbPath = 'Pipeline/tests/testsDB'
dirPath = '%s/%s' % (Settings.BASE_PATH, dbPath)


def test_DailyCapital():
    os.remove('%s/PerformanceLogs/DailyCapitalLog.ujson' % dirPath) if \
        'DailyCapitalLog.ujson' in os.listdir('%s/PerformanceLogs' % dirPath) else None
    DC = DailyCapital(dbPath=dbPath)
    DC.run()
    lastRecord = DC.run()
    assert len(DC.db.all()) == 2
    assert False not in [DC.capitalDict[val[0]] == lastRecord[val[1]] for val in [('liquidCurrent', 'RealCapital'),
                            ('paperCurrent', 'PaperCapital'), ('percentAllocated', 'percentAllocated')]]

