from tinydb import TinyDB
import uuid
import time
import Settings


class DBProp:

    def __init__(
            self,
            gran,
            base='BTC',
            CheapVolParams={
                'numPeriodsVolLong': 100,
                'numPeriodsVolShort': 5,
                'numPeriodsMA': 30,
                'bolStd': 1,
                'volCoef': 1
            },
            ProfitRunParams={
                'minCoef': 0.5,
                'numPeriods': 50,
                'closeAt': 15,
                'stdDict': {
                    'up': 1,
                    'down': 0.5
                },
                'maxRun': True
            },
            dbPath = 'Pipeline/DB'
    ):
        self.gran = gran
        self.base = base
        self.cheapVolParams = CheapVolParams
        self.profitRunParams = ProfitRunParams
        self.configDB = TinyDB('%s/%s/configs/CheapVol_ProfitRun.json' % (Settings.BASE_PATH, dbPath))
        self.perfDB = TinyDB('%s/%s/StratPerformance.json' % (Settings.BASE_PATH, dbPath))
        self.id = str(uuid.uuid4())
        self.addConfigs()
        self.addPerfStrat()

    def addConfigs(self):
        self.configDB.table('CheapVol').insert(self.cheapVolParams)
        self.configDB.table('ProfitRun').insert(self.profitRunParams)
        self.configDB.insert({'gran': self.gran,
                              'assetBase': self.base,
                              'id': self.id
                              })

    def addPerfStrat(self):
        table = self.perfDB.table('CheapVol_ProfitRun_%s_%s' % (self.gran, self.base))
        table.insert({
            'stratName': 'CheapVol_ProfitRun',
            'gran': self.gran,
            'id': self.id,
            'base': 'BTC',
            'assetList': 'all',
            'tsOpen': time.time(),
            'periodsLive': 0,
            'numPositions': 0,
            'histLog': []
        })

DBProp(gran='1d')