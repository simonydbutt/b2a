from tinydb import TinyDB
import os
import Settings


class PaperGains:

    def __init__(self, fees, dbPath='Pipeline/DB/CurrentPositions'):
        self.fees = fees
        dirPath = '%s/%s' % (Settings.BASE_PATH, dbPath)
        self.dbList = [TinyDB('%s/%s' % (dirPath, strat)) for strat in
                    os.listdir(dirPath)]

    def calc(self):
        return round(sum([
            sum([trade['amountHeld'] / trade['currentPrice'] for trade in db.all()])
            for db in self.dbList
        ]),2)

    def allocated(self, liquidCurrent):
        positionCap = self.calc()
        return round(positionCap/(liquidCurrent+positionCap), 4)
