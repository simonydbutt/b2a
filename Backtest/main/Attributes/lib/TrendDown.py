class TrendDown:
    def __init__(self, df, params):
        self.df = df
        self.H = self.df["high"]
        self.L = self.df["low"]
        self.numPeriods = params["numPeriods"] if "numPeriods" in params.keys() else 3
        self.coef = params["coef"] if "coef" in params.keys() else 1
        self.attrName = (
            params["attrName"] if "attrName" in params.keys() else "trendDown"
        )
        self.delay = params["delay"] if "delay" in params.keys() else 0

    def run(self):
        trendList = [False for _ in range(len(self.df))]
        for i in range(self.numPeriods, len(self.df) - self.delay):
            isTrendHigh = False not in [
                True if self.coef * self.H.iloc[j] < self.H.iloc[j - 1] else False
                for j in range(i - self.numPeriods, i)
            ]
            isTrendLow = False not in [
                True if self.coef * self.L.iloc[j] < self.L.iloc[j - 1] else False
                for j in range(i - self.numPeriods, i)
            ]
            trendList[i + self.delay] = isTrendHigh and isTrendLow
        return [(self.attrName, trendList)]
