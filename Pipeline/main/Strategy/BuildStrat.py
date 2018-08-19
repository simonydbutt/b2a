from tinydb import TinyDB
import Settings
import yaml
import os


class BuildStrat:

    def __init__(self, stratName, positionSizeParams, enterParams, exitParams, assetList='all', baseAsset='BTC'):
        dbPath = '%s/Pipeline/DB' % Settings.BASE_PATH
        self.createDirStructure(dbPath=dbPath, stratName=stratName)
        config = {
            'stratName': stratName,
            'baseAsset': baseAsset,
            'assetList': assetList,
            'positionSize': positionSizeParams,
            'enter': enterParams,
            'exit': exitParams
        }
        self.createConfigs(configDict=config)

    def createDirStructure(self, dbPath, stratName):
        for path in [
            dbPath,
            '%s/Configs' % dbPath,
            '%s/CurrentPositions' % dbPath,
            '%s/PerformanceLogs' % dbPath,
            '%s/CodeLogs' % dbPath,
            '%s/CodeLogs/%s' % (dbPath, stratName)
        ]:
            os.mkdir(path) if not os.path.isdir(path) else None

    def createConfigs(self, configDict):
        dbPath = '%s/Pipeline/DB' % Settings.BASE_PATH
        stratName = configDict['stratName']
        response = '0'
        filePath = '%s/Configs/%s.yml' % (Settings.BASE_PATH, stratName)
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
            with open('%s/Configs/%s' % (dbPath, fileName), 'w') as file:
                yaml.dump(configDict, file)
            TinyDB('%s/CurrentPositions/%s.ujson' % (dbPath, stratName))
            print(log)
        else:
            print('No action taken')

BuildStrat(
    stratName='CheapVol_ProfitRun',
    positionSizeParams={'name': 'Basic', 'percent': 0.05},
    enterParams={
        'name': 'CheapVol',
        'exchange': 'Binance',
        'granularity': 14400,
        'periodsVolLong': 100,
        'periodsVolShort': 5,
        'periodsMA': 100,
        'volCoef': 1.5,
        'bolStd': 2
    },
    exitParams={}
)