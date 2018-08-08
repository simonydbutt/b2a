from Pipeline.main.Strategies.CheapVol_ProfitRun.IsCheapVol import IsCheapVol
from Pipeline.main.Strategies.CheapVol_ProfitRun.IsProfitRun import IsProfitRun
from Pipeline.main.PullData.PullBinance import PullBinance
from Pipeline.main.Finance.HistoricalKellyPS import HistoricalKellyPS
from Pipeline.main.Strategies.OpenClosePosition import OpenClosePosition
import datetime
import numpy as np
import yaml
import Settings
from tinydb import TinyDB, Query
import uuid
import time
import logging


class RunStrat:

    def __init__(self, stratName=None, gran='1d', base='BTC', assetList='all',
                 fileLogLevel=logging.INFO, consoleLogLevel=logging.WARNING, fees=0.001,
                 dbPath='Pipeline/DB'):
        self.stratName = 'CheapVol_ProfitRun_%s_%s_%s' % (gran, base, assetList) if not stratName else stratName
        self.fees = fees
        self.dbPath = dbPath
        dTime = datetime.datetime.fromtimestamp(round(time.time())).isoformat()
        logging.basicConfig(
            level=fileLogLevel,
            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            filename='%s/%s/CodeLogs/%s_%s' % (Settings.BASE_PATH, self.dbPath, self.stratName, dTime),
            filemode='w'
        )
        console = logging.StreamHandler()
        console.setLevel(consoleLogLevel)
        logging.getLogger('').addHandler(console)
        with open('%s/%s/Configs/%s.yml' % (Settings.BASE_PATH, self.dbPath, self.stratName)) as configFile:
            self.config = yaml.load(configFile)
        self.P = PullBinance()
        self.HK = HistoricalKellyPS(self.config)
        self.CO = OpenClosePosition(stratName=self.stratName, fees=self.fees)
        self.assetList = self.P.getBTCAssets() if assetList == 'all' else assetList
        self.currentDB = TinyDB('%s/%s/CurrentPositions/%s.ujson' % (Settings.BASE_PATH, self.dbPath, self.config['stratID']))
        self.noActionList = []
        self.enterList = []
        self.exitList = []
        self.openList = []
        self.noDataList = []

    def inPosition(self, asset):
        row = self.P.getCandles(asset=asset, limit=1, interval=self.config['granularity']).iloc[-1]
        close = row['close']
        q = Query()
        tradeParams = self.currentDB.search(q.asset == asset)[0]
        stratParams = self.config['parameters']['ProfitRun']
        returnVal = IsProfitRun(closeVal=close, stratParams=stratParams, tradeParams=tradeParams).run()
        if returnVal < 2:
            self.currentDB.remove(q.asset == asset)
            tradeDict = {
                'asset': asset,
                'stratID': self.config['stratID'],
                'tradeID': tradeParams['tradeID'],
                'granularity': self.config['granularity'],
                'openPrice': tradeParams['openPrice'],
                'closePrice': close,
                'periods': tradeParams['periods'] + 1,
                'capitalAllocated': tradeParams['capAllocated'],
                'TSOpen': tradeParams['TSOpen'],
                'TSClose': row['TS'],
                'amountHeld': tradeParams['amountHeld']
            }
            self.CO.closePosition(tradeDict=tradeDict)
            self.exitList.append(asset)
        elif returnVal == 2:
            self.currentDB.update(
                {
                    'periods': tradeParams['periods'] + 1,
                    'currentPrice': close,
                    'sellPrice': close - tradeParams['std'] * stratParams['stdDict']['down'],
                    'hitPrice': close + tradeParams['std'] * stratParams['stdDict']['up']
                }, q.asset == asset)
            self.openList.append(asset)
        else:
            self.currentDB.update({
                'periods': tradeParams['periods'] + 1,
                'currentPrice': close
            }, q.asset == asset)
            self.openList.append(asset)

    def outPosition(self, asset):
        df = self.P.getCandles(
            asset=asset,
            limit=max(
                self.config['parameters']['CheapVol']['numPeriodsMA'],
                self.config['parameters']['CheapVol']['numPeriodsVolLong']),
            interval=self.config['granularity']
        )
        cVParams = self.config['parameters']['CheapVol']
        if len(df) >= max(cVParams['numPeriodsVolLong'], cVParams['numPeriodsVolShort'], cVParams['numPeriodsMA']):
            if IsCheapVol(df, params=self.config['parameters']['CheapVol']).run():
                params = self.config['parameters']['ProfitRun']
                df = df if len(df) >= params['numPeriods'] else \
                    self.P.getCandles(asset=asset, limit=params['numPeriods'], interval=self.config['granularity'])
                closeVal = df.iloc[-1]['close']
                stdVal = np.std(df[-params['numPeriods']:]['close'])
                positionSize = self.HK.positionSize(self.CO.capitalDict['liquidCurrent'])
                openParams = {
                    'asset': asset,
                    'std': stdVal,
                    'openPrice': closeVal,
                    'currentPrice': closeVal,
                    'tradeID': str(uuid.uuid1()),
                    'sellPrice': closeVal - params['stdDict']['down'] * stdVal,
                    'hitPrice': closeVal + params['stdDict']['up'] * stdVal,
                    'capAllocated': positionSize,
                    'periods': 0,
                    'TSOpen': df.iloc[-1]['TS'],
                    'amountHeld': (positionSize * (1 - self.fees)) * closeVal
                }
                self.CO.openPosition(openParams)
                self.currentDB.insert(openParams)
                self.enterList.append(asset)
            else:
                self.noActionList.append(asset)
        else:
            self.noDataList.append(asset)

    def logResults(self, startTime, endTime):
        logging.info('Time end: %s' % datetime.datetime.fromtimestamp(round(endTime)).isoformat())
        logging.info('Time taken: %ss' % round(endTime - startTime, 2))
        logging.info('%s trades entered' % len(self.enterList))
        if len(self.enterList) != 0:
            logging.info('Entered trades: %s' % [trade for trade in self.enterList])
        logging.info('%s trades exited' % len(self.exitList))
        if len(self.exitList) != 0:
            logging.info('Exited trades: %s' % [trade for trade in self.exitList])
        logging.info('%s trades open' % len(self.openList))
        if len(self.openList) != 0:
            logging.info('Open postions: %s' % [asset for asset in self.openList])
        logging.info('%s assets no action' % len(self.noActionList))
        if len(self.noDataList):
            logging.info('%s assets have not enough data' % len(self.noDataList))
            logging.info('No data assets: %s' % [asset for asset in self.noDataList])

    def run(self):
        start = round(time.time())
        logging.info('Strategy Name: %s' % self.stratName)
        logging.info('Time start: %s' % datetime.datetime.fromtimestamp(start).isoformat())
        logging.info('Num. assets analysed: %s' % len(self.assetList))
        for asset in self.assetList:
            logging.debug(asset)
            if asset in [val['asset'] for val in self.currentDB.all()]:
                self.inPosition(asset=asset)
            else:
                self.outPosition(asset=asset)
            # Doesn't need to be fast so to avoid any rate limit issues
            time.sleep(.5)
        self.CO.add2Books()
        end = time.time()
        logging.info('Run complete')
        self.logResults(startTime=start, endTime=end)
