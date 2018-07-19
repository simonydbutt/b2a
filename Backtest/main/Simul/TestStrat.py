from Backtest.main.Entrance.Enter import Enter
from Backtest.main.Exit.Exit import Exit
from Backtest.main.Utils.AssetBrackets import AssetBrackets
from Backtest.main.Utils.TimeUtil import TimeUtil
from Backtest.main.Visual.StratVisual import StratVisual
import numpy as np


class TestStrat:

    def __init__(self, Entrance, exitStrat, isVisual=False):
        self.E = Entrance
        self.positionDict = Exit(self.E, exitStrat).run()
        print(self.positionDict)
        self.assetList = self.E.assetList
        self.dfDict = self.E.dfDict
        self.ts2Bin = TimeUtil().ts2Bin
        self.isVisual=isVisual

    def run(self):
        resultsDict = {
            asset: {'results': [], 'numPeriods': []} for asset in self.assetList + ['Total']
        }
        resultsDict['Total']['dfSize'] = 0
        for asset in self.assetList:
            df = self.dfDict[asset]
            gran = int(df['TS'].iloc[1] - df['TS'].iloc[0])
            positionList = self.positionDict[asset]
            n = 0
            for position in positionList:
                if position[1] < len(df):
                    result = (df.iloc[position[0]]['close']/df.iloc[position[1]]['close'] - 1)*100
                    resultsDict[asset]['results'].append(result)
                    resultsDict[asset]['numPeriods'].append(position[1] - position[0])
                    resultsDict['Total']['results'].append(result)
                    resultsDict['Total']['numPeriods'].append(position[1] - position[0])
            resultsDict[asset]['gran'] = gran
            resultsDict[asset]['dfSize'] = len(df)
            resultsDict['Total']['dfSize'] += len(df)
        resultsDict['Total']['gran'] = gran
        self.printStats(resultsDict)

    def printStats(self, resultsDict):
        for asset in resultsDict.keys():
            noEntries = len(resultsDict[asset]['results'])
            print('_________________________________')
            print('---------------------------------')
            print('Asset\t\t |\t%s\n'
                  'Granularity\t |\t%s\n'
                  'No. Entries\t |\t%s\n'
                  'Availability |\t%.2f%%\n'
                  '---------------------------------'
                  % (asset, self.ts2Bin[str(resultsDict[asset]['gran'])], noEntries,
                     100*(noEntries/resultsDict[asset]['dfSize'])))
            results = resultsDict[asset]['results']
            periods = resultsDict[asset]['numPeriods']
            if len(results) > 0:
                print('Avg PnL\t\t |\t%.4f%%\n'
                      'Max Profit\t |\t%.4f%%\n'
                      'Max Loss\t |\t%.4f%%\n'
                      'Sharpe Ratio |\t%.2f\n'
                      'Win/Loss\t |\t%.f%%\n'
                    % (
                        float(np.nanmean(results)),
                        float(np.nanmax(results)), float(np.nanmin(results)),
                        float(np.nanmean(results)/np.nanstd(results)) if len(results) != 1 else np.NaN,
                        len([_ for _ in results if _ > 0])*100 / len(results)
                        ))
                print('---------------------------------')
                print('Avg Periods\t |\t%.2f\n'
                      'Max Periods\t |\t%s\n'
                      'Min Periods\t |\t%s\n'
                    % (
                        float(np.nanmean(periods)),
                        float(np.nanmax(periods)),
                        float(np.nanmin(periods))
                        ))
                print('---------------------------------')
            print('_________________________________')
        if self.isVisual:
            S = StratVisual(resultsDict=resultsDict)
            S.periodReturns()


A = AssetBrackets().getBrackets(base='BTC')
E = Enter('binance', A['all'], '2h', stratDict={'IsFeasible': {}},  # 'volDir': 'low'}},
          )  # To start from 2018/01
TestStrat(E, ('ResistanceLoss', {}), isVisual=True).run()
