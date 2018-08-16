import numpy as np


class IsCheapVol:

    def __init__(self, df, params):
        self.row = df.iloc[-1]
        self.row['volL'] = np.mean(df.iloc[-params['numPeriodsVolLong']:]['takerQuoteVol'])
        self.row['volS'] = np.mean(df.iloc[-params['numPeriodsVolShort']:]['takerQuoteVol'])
        bolData = df.iloc[-params['numPeriodsMA']:]['close']
        self.row['bolDown'] = np.mean(bolData) - params['bolStd']*np.std(bolData)
        self.volCoef = params['volCoef']

    def run(self):
        return self.row['volS'] > self.volCoef*self.row['volL'] and self.row['close'] < self.row['bolDown']
