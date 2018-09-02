from tinydb import TinyDB
import Settings
import yaml
import os


class StatsUpdate:

    def __init__(self, dbPath):
        self.dbPath = '%s/%s' % (Settings.BASE_PATH, dbPath)

    def indivStats(self, stratName):
        stratPath = '%s/%s' % (self.dbPath, stratName)
        with open('%s/capital.yml' % stratPath) as capFile:
            stats = yaml.load(capFile)
        currentDb = TinyDB('%s/currentPositions.ujson' % stratPath).all()
        transDb = TinyDB('%s/transactionLogs.ujson' % stratPath).all()
        stats['numberOpen'] = len(currentDb)
        stats['openList'] = [val['assetName'] for val in currentDb]
        stats['numberTransactions'] = len(transDb)
        stats['paperAvgPnL'] = round(stats['paperPnL'] / (stats['numberOpen'] + stats['numberTransactions']), 4) if \
            stats['numberOpen'] + stats['numberTransactions'] != 0 else 0
        return stats

    def _queryDict(self, statsDict, param):
        return sum([statsDict[val][param] for val in statsDict.keys()])

    def compStats(self):
        statsDict = {}
        for stratName in os.listdir(self.dbPath):
            statsDict[stratName] = self.indivStats(stratName)
        totalStats = {
            'numberOpen': self._queryDict(statsDict, 'numberOpen'),
            'initialCapital': self._queryDict(statsDict, 'initialCapital'),
            'liquidCurrent': self._queryDict(statsDict, 'liquidCurrent'),
            'paperCurrent': self._queryDict(statsDict, 'paperCurrent'),
        }
        totalStats['paperPnL'] = round(100*(totalStats['paperCurrent'] / totalStats['initialCapital'] - 1), 4)
        totalStats['percentAllocated'] = 100*round(1 - totalStats['liquidCurrent'] / totalStats['paperCurrent'], 2)
        statsDict['total'] = totalStats
        return statsDict