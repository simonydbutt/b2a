from Backtest.main.Entrance.Enter import Enter
from Backtest.main.Exit.Exit import Exit
from Backtest.main.Utils.AssetBrackets import AssetBrackets
from Backtest.main.Utils.TimeUtil import TimeUtil
import numpy as np


class TestStrat:

    def __init__(self, Entrance, exitStrat):
        self.E = Entrance
        self.positionDict = Exit(self.E, exitStrat).run()
        self.assetList = self.E.assetList
        self.dfDict = self.E.dfDict
        self.ts2Bin = TimeUtil().ts2Bin

    def run(self):
        resultsDict = {
            asset: {'results': []} for asset in self.assetList + ['Total']
        }
        resultsDict['Total']['dfSize'] = 0
        for asset in self.assetList:
            df = self.dfDict[asset]
            gran = int(df['TS'].iloc[1] - df['TS'].iloc[0])
            positionList = self.positionDict[asset]
            n = 0
            for position in positionList:
                result = (df.iloc[position[0]]['close']/df.iloc[position[1]]['close'] - 1)*100
                resultsDict[asset]['results'].append(result)
                resultsDict['Total']['results'].append(result)
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
                  'Availability |\t%.4f\n'
                  '---------------------------------'
                  % (asset, self.ts2Bin[str(resultsDict[asset]['gran'])], noEntries,
                     100*(noEntries/resultsDict[asset]['dfSize'])))
            results = resultsDict[asset]['results']
            if len(results) > 0:
                print('Avg PnL\t\t |\t%.4f%%\n'
                      'Max Profit\t |\t%.4f%%\n'
                      'Max Loss\t |\t%.4f%%\n'
                      'Sharpe Ratio |\t%.2f\n'
                      'Win/Loss\t |\t%.f%%\n'
                    % (
                        float(np.nanmean(results)),
                        float(np.nanmax(results)), float(np.nanmin(results)),
                        float(np.nanmean(results)/np.nanstd(results)),
                        len([_ for _ in results if _ > 0])*100 / len(results)
                        ))
                print('---------------------------------')
            print('_________________________________')



A = AssetBrackets().getBrackets(base='BTC')
print(A['big'])
E = Enter('binance', A['big'], '12h', stratDict={'IsFeasible': {}},  # 'volDir': 'low'}},
          startTime=1514764800)  # To start from 2018/01
TestStrat(E, ('ResistanceLoss', {})).run()
