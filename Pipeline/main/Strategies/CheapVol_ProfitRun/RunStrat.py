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
                 fileLogLevel=logging.INFO, consoleLogLevel=logging.WARNING, fees=0.001):
        self.stratName = 'CheapVol_ProfitRun_%s_%s_%s' % (gran, base, assetList) if not stratName else stratName
        self.fees = fees
        dTime = datetime.datetime.fromtimestamp(round(time.time())).isoformat()
        logging.basicConfig(
            level=fileLogLevel,
            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            filename='%s/Pipeline/DB/CodeLogs/%s_%s' % (Settings.BASE_PATH, self.stratName, dTime),
            filemode='w'
        )
        console = logging.StreamHandler()
        console.setLevel(consoleLogLevel)
        logging.getLogger('').addHandler(console)
        with open('%s/Pipeline/DB/Configs/%s.yml' % (Settings.BASE_PATH, self.stratName)) as configFile:
            self.config = yaml.load(configFile)
        self.P = PullBinance()
        self.HK = HistoricalKellyPS(self.config)
        self.CO = OpenClosePosition(stratName=self.stratName, fees=self.fees)
        self.assetList = self.P.getBTCAssets() if assetList == 'all' else assetList
        self.currentDB = TinyDB('%s/Pipeline/DB/CurrentPositions/%s.ujson' % (Settings.BASE_PATH, self.config['stratID']))

    def run(self):
        startTime = round(time.time())
        logging.info('Strategy Name: %s' % self.stratName)
        logging.info('Time start: %s' % datetime.datetime.fromtimestamp(startTime).isoformat())
        logging.info('Num. assets analysed: %s' % len(self.assetList))
        noActionList = []
        enterList = []
        exitList = []
        openList = []
        noDataList = []
        for asset in self.assetList:
            logging.debug(asset)
            if asset in [val['asset'] for val in self.currentDB.all()]:
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
                        'openFce': tradeParams['openPrice'],
                        'closePrice': close,
                        'periods': tradeParams['periods'] + 1,
                        'capitalAllocated': tradeParams['capAllocated'],
                        'TSOpen': tradeParams['TSOpen'],
                        'TSClose': row['TS'],
                        'amountHeld': tradeParams['amountHeld']
                    }
                    self.CO.closePosition(tradeDict=tradeDict)
                    exitList.append(asset)
                elif returnVal == 2:
                    self.currentDB.update(
                        {
                            'periods': tradeParams['periods'] + 1,
                            'currentPrice': close,
                            'sellPrice': close - tradeParams['std'] * stratParams['stdDict']['down'],
                            'hitPrice': close + tradeParams['std'] * stratParams['stdDict']['up']
                        }, q.asset == asset)
                    openList.append(asset)
                else:
                    self.currentDB.update({
                        'periods': tradeParams['periods'] + 1,
                        'currentPrice': close
                    }, q.asset == asset)
                    openList.append(asset)
            else:
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
                        positionSize = self.HK.size(self.CO.capitalDict['liquidCurrent'])
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
                            'amountHeld': (positionSize*(1-self.fees))*closeVal
                        }
                        self.CO.openPosition(openParams)
                        self.currentDB.insert(openParams)
                        enterList.append(asset)
                    else:
                        noActionList.append(asset)
                else:
                    noDataList.append(asset)
            # Doesn't need to be fast so to avoid any rate limit issues
            time.sleep(.5)
        self.CO.add2Books()
        endTime = time.time()
        logging.info('Run complete')
        logging.info('Time end: %s' % datetime.datetime.fromtimestamp(round(endTime)).isoformat())
        logging.info('Time taken: %ss' % round(endTime - startTime, 2))
        logging.info('%s trades entered' % len(enterList))
        if len(enterList) != 0:
            logging.info('Entered trades: %s' % [trade for trade in enterList])
        logging.info('%s trades exited' % len(exitList))
        if len(exitList) != 0:
            logging.info('Exited trades: %s' % [trade for trade in exitList])
        logging.info('%s trades open' % len(openList))
        if len(openList) != 0:
            logging.info('Open postions: %s' % [asset for asset in openList])
        logging.info('%s assets no action' % len(noActionList))
        if len(noDataList):
            logging.info('%s assets have not enough data' % len(noDataList))
            logging.info('No data assets: %s' % [asset for asset in noDataList])


RunStrat(gran='5m', consoleLogLevel=logging.INFO).run()