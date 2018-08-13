from tinydb import TinyDB
import os
import Settings
import itertools


class PaperGains:

    """
        TODO: change name to analyseOpenTrades as what it's turning into...
    """

    def __init__(self, fees=.001, dbPath='Pipeline/DB/CurrentPositions', baseStrat='all'):
        dbCompPath = '%s/%s' % (Settings.BASE_PATH, dbPath)
        self.fees = fees
        dirPath = '%s' % dbCompPath if baseStrat == 'all' \
            else '%s/%s' % (dbCompPath, baseStrat)
        self.dbList = [TinyDB('%s/%s' % (dirPath, strat)) for strat in os.listdir(dirPath)] if baseStrat != 'all' \
            else list(itertools.chain.from_iterable([
            [
                TinyDB('%s/%s/%s' % (dirPath, bStrat, strat))
                for strat in os.listdir('%s/%s' % (dirPath, bStrat))
            ] for bStrat in os.listdir(dirPath)]
        ))

    def calc(self):
        return round(sum([
            sum([trade['amountHeld'] / trade['currentPrice'] for trade in db.all()])
            for db in self.dbList
        ]),2)

    def allocated(self, liquidCurrent):
        positionCap = self.calc()
        return round(positionCap/(liquidCurrent+positionCap), 4)

    def numOpenTrades(self):
        return sum([len(db.all()) for db in self.dbList])

