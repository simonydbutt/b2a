from tinydb import TinyDB, Query
import os
import Settings


class PaperGainz:

    def __init__(self, fees):
        self.fees = fees
        dirPath = '%s/Pipeline/DB/CurrentPositions' % Settings.BASE_PATH
        self.dbList = [TinyDB('%s/%s' % (dirPath, strat)) for strat in
                    os.listdir(dirPath)]

    def calc(self):
        return sum([
            sum([trade['capitalAllocated'] * ((1 - self.fees) * trade['currentPrice'] - (1 + self.fees) * trade['openPrice'])
                 for trade in db.all()]) for db in self.dbList
        ])

    def allocated(self):
        return sum([
            sum([trade['capitalAllocated'] for trade in db.all()]) for db in self.dbList
        ])
