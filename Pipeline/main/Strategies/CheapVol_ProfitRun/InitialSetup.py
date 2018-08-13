from Pipeline.main.Utils.SetupUtil import SetupUtil
import uuid
import Settings


class InitialSetup:

    def __init__(
            self,
            gran,
            base='BTC',
            assetList='all',
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
                'maxRun': True,
            },
            KellyParams={
                'coef': 0.5,
                'adv': 0.1
            }
    ):
        stratName = 'CheapVol_ProfitRun_%s_%s_%s' % (gran, base, assetList)
        self.stratID = str(uuid.uuid4())
        self.configDict = {
            'stratID': self.stratID,
            'stratName': stratName,
            'baseAsset': base,
            'assetList': assetList,
            'granularity': gran,
            'parameters': {
                'CheapVol': CheapVolParams,
                'ProfitRun': ProfitRunParams
            },
            'performance': {
                'percentPnL': 0,
                'maxGain': 0,
                'maxLoss': 0,
                'numTrades': 0,
                'winLoss': 0,
                'avgPeriods': 0
            },
            'kelly': KellyParams
        }
        SetupUtil().createConfigs(configDict=self.configDict, baseStrat='CheapVol_ProfitRun', stratName=stratName)

