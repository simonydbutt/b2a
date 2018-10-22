from Backtest.main.Attributes.Attr import Attr
from Backtest.main.Data.Load import Load


class ResistanceLoss:

    """
        Take loss when close < resistance10
        Take profit when openT < close < MA3
    """

    def __init__(self, df, params, enterList, isDebug=False):
        self.numMAPeriods = (
            params["numMAPeriods"] if "numMAPeriods" in params.keys() else 5
        )
        self.numRPeriods = (
            params["numRPeriods"] if "numRPeriods" in params.keys() else 10
        )
        self.coef = params["coef"] if "coef" in params.keys() else 0.99
        self.df = Attr(
            Attr(df).add(
                "MA", params={"attrName": "exitMA", "numPeriods": self.numMAPeriods}
            )
        ).add("Support", params={"numPeriods": self.numRPeriods})
        self.enterList = enterList
        self.isDebug = isDebug

    def getIndex(self, df, TSVal):
        return df.index[df["TS"] == TSVal].tolist()[0]

    def run(self):
        positionList = []
        for val in self.enterList:
            pos = self.getIndex(self.df, val)
            buyAt = self.df.iloc[pos]["close"]
            # print('\n%s' % buyAt)
            periods = 1
            while periods < 50 and pos + periods < len(self.df):
                row = self.df.iloc[pos + periods]
                if row["close"] < row["support"]:
                    if self.isDebug:
                        print(1)
                    break
                elif row["close"] < self.coef * row["exitMA"] and row["close"] > buyAt:
                    if self.isDebug:
                        print(1)
                    break
                else:
                    periods += 1
            if self.isDebug:
                print(str(round(100 * (row["close"] / buyAt - 1), 2)) + "%")
            positionList.append((pos, pos + periods))
        return positionList


# df = Load(dbName='binance').loadOne('BCCBTC_2h', timeStart=1483228800, timeEnd=1527811200)
# enterList = [1513324800.0, 1514304000.0, 1514764800.0, 1515139200.0]
#
# R = ResistanceLoss(df=df, enterList=enterList, params={'numMAPeriods': 5, 'numRPeriods': 10, 'coef': 0.99}, isDebug=True)
# l = R.run()
# print([a[1] - a[0] for a in l])
