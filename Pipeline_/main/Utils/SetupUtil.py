import os
from tinydb import TinyDB
import Settings
import yaml


class SetupUtil:

    def createDirStructure(self, dbPath, baseStratName):
        for path in [
            dbPath,
            '%s/Configs' % dbPath,
            '%s/Configs/%s' % (dbPath, baseStratName),
            '%s/CurrentPositions' % dbPath,
            '%s/CurrentPositions/%s' % (dbPath, baseStratName),
            '%s/PerformanceLogs' % dbPath,
            '%s/PerformanceLogs/%s' % (dbPath, baseStratName),
            '%s/PerformanceLogs/%s/StratLogs' % (dbPath, baseStratName),
            '%s/CodeLogs' % dbPath,
            '%s/CodeLogs/%s' % (dbPath, baseStratName)
        ]:
            os.mkdir(path) if not os.path.isdir(path) else None

    def createConfigs(self, configDict, baseStrat, stratName):
        response = '0'
        filePath = '%s/Pipeline_/DB/Configs/%s/%s.yml' % (Settings.BASE_PATH, baseStrat, stratName)
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
            with open('%s/Pipeline_/DB/Configs/%s/%s' % (Settings.BASE_PATH, baseStrat, fileName), 'w') as file:
                yaml.dump(configDict, file)
            TinyDB('%s/Pipeline_/DB/CurrentPositions/%s/%s.ujson' %
                   (Settings.BASE_PATH, baseStrat, configDict['stratID']))
            TinyDB('%s/Pipeline_/DB/PerformanceLogs/%s/StratLogs/%s.ujson' %
                   (Settings.BASE_PATH, baseStrat, configDict['stratID']))
            print(log)
        else:
            print('No action taken')