from tinydb import TinyDB
import Settings
import shutil
import yaml
import os


class Clean:

    def __init__(self, db, stratName, archivePath=False):
        self.path = '%s/Pipeline/DB/%s/%s' % (Settings.BASE_PATH, db, stratName)

    def cleanStrat(self):
        shutil.rmtree(self.path)

    def resetStrat(self):
        with open('%s/capital.yml' % self.path, 'r') as capFile:
            initCap = yaml.load(capFile)['initialCapital']
        with open('%s/capital.yml' % self.path, 'w') as capFile:
            yaml.dump(
                data={'initialCapital': initCap, 'liquidCurrent': initCap, 'paperCurrent': initCap,
                      'paperPnL': 0, 'percentAllocated': 0},
                stream=capFile
            )
            capFile.close()
        shutil.rmtree('%s/CodeLogs' % self.path)
        os.remove('%s/currentPositions.ujson' % self.path)
        os.remove('%s/transactionLogs.ujson' % self.path)
        os.mkdir('%s/CodeLogs' % self.path)
        TinyDB('%s/currentPositions.ujson' % self.path)
        TinyDB('%s/transactionLogs.ujson' % self.path)



# Clean(db='disco', stratName='CheapVol_ProfitRun').resetStrat()