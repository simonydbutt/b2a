import Settings
import os
import yaml
import shutil


class Clean:

    def __init__(self, stratName, fullSweep=False):
        dbPath = '%s/Pipeline/DB' % Settings.BASE_PATH
        if fullSweep:
            shutil.rmtree(dbPath)
        else:
            stratList = os.listdir('%s/Configs' % dbPath) if stratName == 'all' else ['%s.yml' % stratName]
            for stratFileName in stratList:
                with open('%s/Configs/%s' % (dbPath, stratFileName)) as configFileName:
                    stratID = yaml.load(configFileName)['stratID']
                os.remove('%s/Configs/%s' % (dbPath, stratFileName))
                os.remove('%s/CurrentPositions/%s.ujson' % (dbPath, stratID))
                os.remove('%s/PerformanceLogs/StratLogs/%s.ujson' % (dbPath, stratID))
                for file in [file for file in os.listdir('%s/CodeLogs' % dbPath) if stratFileName[:-4] in file]:
                    os.remove('%s/CodeLogs/%s' % (dbPath, file))


Clean(stratName='all', fullSweep=True)