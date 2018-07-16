from Backtest.main.Entrance.Enter import Enter
from Backtest.main.Utils.TimeUtil import TimeUtil
from Backtest.main.Utils.AssetBrackets import AssetBrackets
import numpy as np


class TestEntry:

    """
        Tests entrance strategies class:Enter over a number of time periods with result visualisation
    """

    def __init__(self, EntryStrat, periodList=(5, 10, 15)):
        self.periodList = periodList
        self.E = EntryStrat
        self.ts2Bin = TimeUtil().ts2Bin
        self.assetList = self.E.assetList
        self.enterAtDict = self.E.run()
        self.dfDict = self.E.dfDict

    def getVal(self, df, TS):
        val = df.loc[df['TS'] == int(TS)]['close'].values
        return val[0] if len(val) == 1 else np.NaN

    def getDD(self, df, tsStart, tsEnd):
        df_ = df.loc[(df['TS'] >= int(tsStart)) & (df['TS'] <= int(tsEnd))]['low']
        return np.nanmin(df_.values)

    def run(self):
        resultsDict = {
            asset: {str(period): [[],[]] for period in self.periodList} for asset in self.assetList + ['Total']
        }
        resultsDict['Total']['dfSize'] = 0
        for asset in self.assetList:
            df = self.dfDict[asset]
            print(asset)
            print(len(df))
            gran = int(df['TS'].iloc[1] - df['TS'].iloc[0])
            enterList = self.enterAtDict[asset]
            n = 0
            for position in enterList:
                if position + max(self.periodList)*gran <= df['TS'].iloc[-1]:
                    val = self.getVal(df, position)
                    for period in self.periodList:
                        resultsDict[asset][str(period)][0].append(
                            round(100*(self.getVal(df, position + gran*period)/val - 1), 6)
                        )
                        resultsDict[asset][str(period)][1].append(
                            round(100*(self.getDD(df, position, position+gran*period)/val - 1), 6)
                        )
                        resultsDict['Total'][str(period)][0].append(
                            round(100 * (self.getVal(df, position + gran * period) / val - 1), 6)
                        )
                        resultsDict['Total'][str(period)][1].append(
                            round(100 * (self.getDD(df, position, position + gran * period) / val - 1), 6)
                        )
            resultsDict[asset]['gran'] = gran
            resultsDict[asset]['dfSize'] = len(df)
            resultsDict['Total']['dfSize'] += len(df)
        resultsDict['Total']['gran'] = gran
        print(resultsDict)
        self.printStats(resultsDict)

    def printStats(self, resultsDict):
        for asset in resultsDict.keys():
            noEntries = len(list(resultsDict[asset].values())[0][0])
            print('_________________________________')
            print('---------------------------------')
            print('Asset\t\t |\t%s\n'
                  'Granularity\t |\t%s\n'
                  'No. Entries\t |\t%s\n'
                  'Availability |\t%.4f\n'
                  '---------------------------------'
                  % (asset, self.ts2Bin[str(resultsDict[asset]['gran'])], noEntries,
                     100*(noEntries/resultsDict[asset]['dfSize'])))
            for period in [p for p in resultsDict[asset].keys() if p != 'gran' and p != 'dfSize']:
                results = resultsDict[asset][period][0]
                if len(results) > 0:
                    ddList = resultsDict[asset][period][1]
                    print('Period\t\t |\t%s\n'
                          'Avg PnL\t\t |\t%.4f%%\n'
                          'Max Profit\t |\t%.4f%%\n'
                          'Max Loss\t |\t%.4f%%\n'
                          'Sharpe Ratio |\t%.2f\n'
                          'Win/Loss\t |\t%.f%%\n'
                          'Av Drawdown\t |\t%.4f%%\n'
                          'Max Drawdown |\t%.4f%%\n'
                          % (
                            period, float(np.nanmean(results)),
                            float(np.nanmax(results)), float(np.nanmin(results)),
                            float(np.nanmean(results)/np.nanstd(results)),
                            len([_ for _ in results if _ > 0])*100 / len(results),
                            float(np.nanmean(ddList)), float(np.nanmin(ddList))
                            ))
                print('---------------------------------')
            print('_________________________________')


A = AssetBrackets().getBrackets(base='BTC')
E = Enter('binance', A['all'], '12h', stratDict={'IsFeasible': {}})

TestEntry(E).run()
