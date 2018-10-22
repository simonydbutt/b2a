from Backtest.main.Attributes.Attr import Attr


class LadderBottom:

    """
        Three consecutive down periods followed by a gap white

        ** Not promising
    """

    def __init__(self, df, params):
        self.gapCoef = params["gapCoef"] if "gapCoef" in params.keys() else 1.005
        self.gapPeriods = params["gapPeriods"] if "gapPeriods" in params.keys() else 2
        self.numBSPeriods = (
            params["numBSPeriods"] if "numBSPeriods" in params.keys() else 3
        )
        self.df = Attr(
            Attr(df).add(
                "UpGap", params={"numPeriods": self.gapPeriods, "coef": self.gapCoef}
            )
        ).add("BlackSoldiers", params={"numPeriods": self.numBSPeriods, "delay": 1})

    def run(self):
        self.df["ladderBottom"] = self.df.apply(self.conditions, axis=1)
        return list(self.df[self.df["ladderBottom"]]["TS"].values)

    def conditions(self, row):
        return False not in [row["blackSoldiers"], row["upGap"]]
