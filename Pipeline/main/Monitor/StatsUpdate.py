from pymongo import MongoClient
import pandas as pd
import Settings
import logging
import yaml
import os


class StatsUpdate:

    """
        *TODO: create some semblance of normality with stats format...
    """

    def __init__(self):
        logging.debug('Initialising StatsUpdate()')
        self.client = MongoClient('localhost', 27017)

    def indivStats(self, stratName):
        logging.debug('Starting StatsUpdate.indivStats')
        with open('%s/Pipeline/resources/%s/capital.yml' % (Settings.BASE_PATH, stratName)) as capFile:
            stats = yaml.load(capFile)
        currentCol = self.client[stratName]['currentPositions']
        transCol = self.client[stratName]['transactionLogs']
        stats['numberOpen'] = currentCol.count()
        stats['openList'] = [val['assetName'] for val in list(currentCol.find())]
        stats['numberTransactions'] = transCol.count()
        stats['paperAvgPnL'] = round(stats['paperPnL'] / (stats['numberOpen'] + stats['numberTransactions']), 4) if \
            stats['numberOpen'] + stats['numberTransactions'] != 0 else 0
        logging.debug('Ending indivStats')
        return stats

    def _queryDict(self, statsDict, param):
        logging.debug('Starting StatsUpdate._queryDict')
        return sum([statsDict[val][param] for val in statsDict.keys()])

    def compStats(self, isTest=None):
        logging.debug('Starting StatsUpdate.compStats')
        statsDict = {}
        stratList = [val for val in os.listdir('%s/Pipeline/resources' % Settings.BASE_PATH) if val != '__init__.py'] \
            if not isTest else isTest
        for stratName in stratList:
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
        logging.debug('Ending compStats')
        return statsDict

    def getCurrentStats(self, stratName):
        logging.debug('Starting StatsUpdate.getCurrentStats')
        df = pd.DataFrame(
            list(self.client[stratName].currentPositions.find(
                {},
                {
                    '_id': 0,
                    'assetName': 1,
                    'openPrice': 1,
                    'currentPrice': 1,
                    'periods': 1
                }
            ))
        )
        df['daysOpen'] = round(df['periods'] / 48, 2)
        df.drop('periods', axis=1, inplace=True)
        df['%'] = 100 * round(df['currentPrice'] / df['openPrice'], 4)
        return df
