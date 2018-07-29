from Pipeline.main.Strategies.CheapVol_ProfitRun.IsCheapVol import IsCheapVol
from Pipeline.main.Strategies.CheapVol_ProfitRun.IsProfitRun import IsProfitRun
from Pipeline.main.PullData.PullBinance import PullBinance
from Pipeline.main.Finance.HistoricalKellyPS import HistoricalKellyPS
from Pipeline.main.Strategies.CloseOut import CloseOut
import numpy as np
import yaml
import Settings
from tinydb import TinyDB, Query
import uuid


class RunStrat:

    def __init__(self, gran='1d', base='BTC', assetList='all', verbose=False):
        self.verbose = verbose
        stratName = 'CheapVol_ProfitRun_%s_%s_%s' % (gran, base, assetList)
        with open('%s/Pipeline/DB/configs/%s.yml' % (Settings.BASE_PATH, stratName)) as configFile:
            self.config = yaml.load(configFile)
        self.P = PullBinance()
        self.HK = HistoricalKellyPS(self.config)
        self.CO = CloseOut(stratName=stratName)
        self.assetList = self.P.getBTCAssets() if assetList == 'all' else assetList
        self.currentDB = TinyDB('%s/Pipeline/DB/CurrentPositions/%s.ujson' % (Settings.BASE_PATH, self.config['stratID']))

    def run(self):
        for asset in self.assetList:
            print(asset)
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
                        'openPrice': tradeParams['openPrice'],
                        'closePrice': close,
                        'periods': tradeParams['periods'] + 1,
                        'capitalAllocated': tradeParams['capAllocated'],
                        'TSOpen': tradeParams['TSOpen'],
                        'TSClose': row['TS']
                    }
                    print('Position %s closed' % asset)
                    self.CO.closePosition(tradeDict=tradeDict)
                elif returnVal == 2:
                    self.currentDB.update(
                        {
                            'periods': tradeParams['periods'] + 1,
                            'currentPrice': close,
                            'sellPrice': close - tradeParams['std'] * stratParams['stdDict']['down'],
                            'hitPrice': close + tradeParams['std'] * stratParams['stdDict']['up']
                        }, q.asset == asset)
                else:
                    self.currentDB.update({
                        'periods': tradeParams['periods'] + 1,
                        'currentPrice': close
                    }, q.asset == asset)
            else:
                df = self.P.getCandles(
                    asset=asset,
                    limit=max(
                        self.config['parameters']['CheapVol']['numPeriodsMA'],
                        self.config['parameters']['CheapVol']['numPeriodsVolLong']),
                    interval=self.config['granularity']
                )
                if IsCheapVol(df, params=self.config['parameters']['CheapVol']).run():
                    params = self.config['parameters']['ProfitRun']
                    df = df if len(df) >= params['numPeriods'] else \
                        self.P.getCandles(asset=asset, limit=params['numPeriods'], interval=self.config['granularity'])
                    closeVal = df.iloc[-1]['close']
                    stdVal = np.std(df[-params['numPeriods']:]['close'])
                    self.currentDB.insert({
                        'asset': asset,
                        'std': stdVal,
                        'openPrice': closeVal,
                        'currentPrice': closeVal,
                        'tradeID': str(uuid.uuid1()),
                        'sellPrice': closeVal - params['stdDict']['down'] * stdVal,
                        'hitPrice': closeVal + params['stdDict']['up'] * stdVal,
                        'capAllocated': self.HK.size(self.CO.capitalDict['liquidCurrent']),
                        'periods': 0,
                        'TSOpen': df.iloc[-1]['TS']
                    })
        self.CO.add2Books()


RunStrat().run()