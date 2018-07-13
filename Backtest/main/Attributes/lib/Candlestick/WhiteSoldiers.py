class WhiteSoldiers:

    def __init__(self, df, params):
        self.df = df
        self.attrName = params['attrName'] if 'attrName' in list(params.keys()) else 'whiteSoldiers'
        self.delay = params['delay'] if 'delay' in list(params.keys()) else 0
        self.numPeriods = params['numPeriods'] if 'numPeriods' in list(params.keys()) else 3

    def run(self):
        wsList = [False for _ in range(len(self.df))]
        for i in range(self.numPeriods + self.delay, len(self.df)):
            isIncrease = False not in [True if self.df['close'].iloc[j] > self.df['close'].iloc[j - 1] else False
                                        for j in range(i - self.numPeriods-self.delay, i-self.delay)]
            isWhite = False not in [True if self.df['close'].iloc[j] > self.df['open'].iloc[j] else False
                                    for j in range(i-self.numPeriods-self.delay, i-self.delay)]
            wsList[i] = isIncrease + isWhite
        return [(self.attrName, wsList)]