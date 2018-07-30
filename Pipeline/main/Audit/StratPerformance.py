from tinydb import TinyDB, Query
import numpy as np
import yaml
import os
import time
import datetime
import Settings


class StratPerformance:

    def __init__(self):
        dbPath = '%s/Pipeline/DB' % Settings.BASE_PATH
        self.stratDict = {

        }
        transDB = TinyDB('%s/TransactionLog.ujson' % dbPath)
        for stratFileName in os.listdir('%s/Configs' % dbPath):
            stratName = stratFileName[:-4]
            with open('%s/Configs/%s' % (dbPath, stratFileName)) as configFile:
                config = yaml.load(configFile)
            q = Query
            currentTrades = TinyDB('%s/CurrentPositions/%s.ujson' % (dbPath, config['stratID'])).all()
            logDB = TinyDB('%s/PerformanceLogs/StratLogs/%s.ujson' % (dbPath, config['stratID']))
            transLog = transDB.search(q.StratID == config['StratID']) if len(transDB.all()) != 0 else []
            pastLog = logDB.all()[-1] if len(logDB.all()) != 0 else {'daysLive': 0, 'percentPnL': 0}
            stratLog = config['performance']
            stratLog['timestamp'] = round(time.time())
            stratLog['dateTime'] = datetime.datetime.fromtimestamp(round(time.time())).isoformat()
            stratLog['daysLive'] = pastLog['daysLive'] + 1
            stratLog['changePnL'] = pastLog['percentPnL'] - stratLog['percentPnL']
            tradePnLList = [trade['percentPnL'] for trade in transLog]
            stratLog['sharpeRatio'] = float(np.mean(tradePnLList)/np.std(tradePnLList)) if len(tradePnLList) != 0 else 0
            stratLog['numCurrent'] = len(currentTrades)
            stratLog['currentList'] = [trade['asset'] for trade in currentTrades]
            logDB.insert(stratLog)

StratPerformance()