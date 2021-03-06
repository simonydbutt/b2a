from Backtest.main.Exit.Exit import Exit
from Backtest.main.Utils.TimeUtil import TimeUtil
from Backtest.main.Visual.StratVisual import StratVisual
from Backtest.main.Utils.AssetBrackets import AssetBrackets
from Backtest.main.Entrance.Enter import Enter
import numpy as np


class TestStrat:
    def __init__(self, Entrance, exitStrat, isVisual=False, verbose=False):
        self.E = Entrance
        self.positionDict = Exit(self.E, exitStrat).run()
        print(self.positionDict)
        self.assetList = self.E.assetList
        self.dfDict = self.E.dfDict
        self.ts2Bin = TimeUtil().ts2Bin
        self.isVisual = isVisual
        self.verbose = verbose

    def run(self):
        resultsDict = {
            asset: {"results": [], "numPeriods": []}
            for asset in self.assetList + ["Total"]
        }
        resultsDict["Total"]["dfSize"] = 0
        for asset in self.assetList:
            df = self.dfDict[asset]
            gran = int(df["TS"].iloc[1] - df["TS"].iloc[0])
            positionList = self.positionDict[asset]
            n = 0
            for position in positionList:
                if position[1] < len(df):
                    result = (
                        df.iloc[position[1]]["close"] / df.iloc[position[0]]["close"]
                        - 1
                    ) * 100
                    resultsDict[asset]["results"].append(result)
                    resultsDict[asset]["numPeriods"].append(position[1] - position[0])
                    resultsDict["Total"]["results"].append(result)
                    resultsDict["Total"]["numPeriods"].append(position[1] - position[0])
            resultsDict[asset]["gran"] = gran
            resultsDict[asset]["dfSize"] = len(df)
            resultsDict["Total"]["dfSize"] += len(df)
        resultsDict["Total"]["gran"] = gran
        self.printStats(resultsDict)

    def printStats(self, resultsDict):
        printList = resultsDict.keys() if self.verbose else ["Total"]
        for asset in printList:
            noEntries = len(resultsDict[asset]["results"])
            print("_________________________________")
            print("---------------------------------")
            print(
                "Asset\t\t |\t%s\n"
                "Granularity\t |\t%s\n"
                "No. Entries\t |\t%s\n"
                "Availability |\t%.2f%%\n"
                "---------------------------------"
                % (
                    asset,
                    self.ts2Bin[str(resultsDict[asset]["gran"])],
                    noEntries,
                    100 * (noEntries / resultsDict[asset]["dfSize"]),
                )
            )
            results = resultsDict[asset]["results"]
            periods = resultsDict[asset]["numPeriods"]
            if len(results) > 0:
                print(
                    "Avg PnL\t\t |\t%.4f%%\n"
                    "Max Profit\t |\t%.4f%%\n"
                    "Max Loss\t |\t%.4f%%\n"
                    "Sharpe Ratio |\t%.2f\n"
                    "Win/Loss\t |\t%.f%%\n"
                    % (
                        float(np.nanmean(results)),
                        float(np.nanmax(results)),
                        float(np.nanmin(results)),
                        float(np.nanmean(results) / np.nanstd(results))
                        if len(results) != 1
                        else np.NaN,
                        len([_ for _ in results if _ > 0]) * 100 / len(results),
                    )
                )
                print("---------------------------------")
                print(
                    "Mean Periods |\t%.2f\n"
                    "Med. Periods |\t%s\n"
                    "Max Periods\t |\t%s\n"
                    "Min Periods\t |\t%s\n"
                    % (
                        float(np.nanmean(periods)),
                        float(np.median(periods)),
                        float(np.nanmax(periods)),
                        float(np.nanmin(periods)),
                    )
                )
                print("---------------------------------")
            print("_________________________________")
        if self.isVisual:
            S = StratVisual(resultsDict=resultsDict)
            S.periodReturns()


A = AssetBrackets(exchangeName="binance").getBrackets(base="BTC")


print("Number assets: %s" % len(A["small"]))
E = Enter(
    "binance",
    A["small"],
    "6h",
    stratDict={
        "IsFeasible": {
            "periodsVolLong": 50,
            "periodsVolShort": 5,
            "numPeriodsMA": 50,
            "volCoef": 1.3,
            "numStd": 1.6,
        }
    },
)
TestStrat(
    E,
    (
        "StdExit",
        {
            "numPeriods": 50,
            "closeAt": 50,
            "stdDict": {"up": 0.25, "down": 2},
            "maxRun": True,
        },
    ),
    isVisual=True,
).run()
