from tinydb import TinyDB
import uuid
import yaml
import os
import Settings


class InitalSetup:

    """
        For performance, calc all but the daysLive and sharpeRatio which are calced in
        daily audit
    """

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
            'kelly': {
                'coef': 0.5,
                'crit': 0.1
            }
        }
        filePath = '%s/Pipeline/DB/Configs/%s.yml' % (Settings.BASE_PATH, stratName)
        response = '0'
        if os.path.exists(filePath):
            print('Config file already exists')
            print('User input required:')
            print('1   \t-\tReplace existing file')
            print('2   \t-\tCreate _2 file')
            print('Else\t-\tIgnore request')
            response = str(input())

        if response == '1' or response == '2' or response == '0':
            log = 'Config Replaced' if response == '1' else 'Config Created'
            fileName = '%s_2.yml' % stratName if response == '2' else '%s.yml' % stratName
            with open('%s/Pipeline/DB/Configs/%s' % (Settings.BASE_PATH, fileName), 'w') as file:
                yaml.dump(self.configDict, file)
            TinyDB('%s/Pipeline/DB/CurrentPositions/%s.ujson' % (Settings.BASE_PATH, self.stratID))
            TinyDB('%s/Pipeline/DB/PerformanceLogs/StratLogs/%s.ujson' % (Settings.BASE_PATH, self.stratID))
            print(log)
        else:
            print('No action taken')


InitalSetup(gran='1d')
