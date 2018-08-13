import Settings
import os
import yaml
import shutil


class Clean:

    def __init__(self, stratName, fullSweep=False):
        dbPath = '%s/Pipeline/DB' % Settings.BASE_PATH
        if fullSweep:
            if input('This will wipe whole DB, type 1 to confirm: ') == '1':
                if os.path.exists(dbPath):
                    shutil.rmtree(dbPath)
                    print('DB Cleaned')
                else:
                    print('DB already cleaned')
        else:
            for dir in ['CodeLogs', 'Configs', 'CurrentPositions', 'PerformanceLogs']:
                path = '%s/%s/%s' % (dbPath, dir, stratName)
                shutil.rmtree(path) if os.path.exists(path) else None
            print('Strat: %s cleaned' % stratName)


Clean(stratName='CommitValue')