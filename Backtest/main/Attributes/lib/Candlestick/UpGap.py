class UpGap:

    def __init__(self, df, params):
        self.df = df
        self.attrName = params['gap'] if 'attrName' in params.keys() else 'upGap'
        self.numPeriods = params['numPeriods'] if 'numPeriods' in params.keys() else 1
        self.coef = params['coef'] if 'coef' in params.keys() else 1.005

    def run(self):
        gapList = [False for _ in range(len(self.df))]
        for i in range(self.numPeriods, len(self.df)):
            isGap = self.df['open'].iloc[i] > self.coef*max(list(self.df['open'].iloc[i-self.numPeriods:i]) +
                                                    list(self.df['close'].iloc[i-self.numPeriods:i]))
            isWhite = self.df['open'].iloc[i] < self.df['close'].iloc[i]
            gapList[i] = False not in [isGap, isWhite]
        return [(self.attrName, gapList)]