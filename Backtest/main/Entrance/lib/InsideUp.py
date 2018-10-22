from Backtest.main.Attributes.Attr import Attr


class InsideUp:

    """
        Pairs a Bull Squeeze candlestick formation with a confirming white session
        numPeriods > 2 then -> squeeze

        12h/1d effective
    """

    def __init__(self, df, params):
        self.condList = (
            params["condList"] if "condList" in params.keys() else ("maBelow", "conf")
        )
        self.numPeriods = params["numPeriods"] if "numPeriods" in params.keys() else 2
        self.maLong = params["maLong"] if "maLong" in params.keys() else 50
        self.maShort = params["maShort"] if "maShort" in params.keys() else 10
        self.df = Attr(
            Attr(
                Attr(df).add("BullSqueeze", params={"numPeriods": self.numPeriods})
            ).add("MA", params={"numPeriods": self.maLong, "attrName": "maLong"})
        ).add("MA", params={"numPeriods": self.maShort, "attrName": "maShort"})
        self.df["maBelow"] = self.df["maLong"] > self.df["maShort"]
        self.df["conf"] = self.df["close"] > self.df["bullConf"]

    def run(self):
        self.df["bullSqueezeConf"] = self.df.apply(self.conditions, axis=1)
        return list(self.df[self.df["bullSqueezeConf"]]["TS"].values)

    def conditions(self, row):
        return False not in [row[val] for val in self.condList] + [row["bullSqueeze"]]
