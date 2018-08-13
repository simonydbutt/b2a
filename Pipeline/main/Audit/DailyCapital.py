from Pipeline.main.Finance.PaperGains import PaperGains
from tinydb import TinyDB
import yaml
import Settings
import time
import datetime


class DailyCapital:

    def __init__(self, dbPath='Pipeline/DB'):
        self.dbPath = dbPath
        self.dirPath = '%s/%s' % (Settings.BASE_PATH, dbPath)
        with open('%s/Capital.yml' % self.dirPath) as capFile:
            self.capitalDict = yaml.load(capFile)
        self.db = TinyDB('%s/PerformanceLogs/DailyCapitalLog.ujson' % self.dirPath)

    def run(self):
        lastPaperCap = self.db.all()[-1]['PaperCapital'] if len(self.db.all()) != 0 else self.capitalDict['initialCapital']
        numOpen = PaperGains(dbPath='%s/CurrentPositions' % self.dbPath).numOpenTrades()
        dailyCapLog = {
            'TS': round(time.time()),
            'Date': datetime.datetime.fromtimestamp(round(time.time())).isoformat(),
            'RealCapital': self.capitalDict['liquidCurrent'],
            'PaperCapital': self.capitalDict['paperCurrent'],
            'percentAllocated': self.capitalDict['percentAllocated'],
            'dailyPerformance': self.capitalDict['paperCurrent'] / lastPaperCap - 1,
            'runningPerformance': self.capitalDict['paperCurrent'] / self.capitalDict['initialCapital'] - 1,
            'numOpenTrades': numOpen,
        }
        self.db.insert(dailyCapLog)
        return dailyCapLog
