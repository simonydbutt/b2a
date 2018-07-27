import numpy as np


class IsCheapVol:

    def __init__(self, df, params):
        self.row = df.iloc[-1]
        self.row['volL'] = np.mean(df.iloc[-params['volMALongPeriods']:]['takerQuoteVol'])
        self.row['volS'] = np.mean(df.iloc[-params['volMAShortPeriods']:]['takerQuoteVol'])
        bolData = df.iloc[-params['maPeriods']:]['close']
        self.row['bolDown'] = np.mean(bolData) - params['bolStd']*np.std(bolData)
        self.volCoef = params['volCoef']

    def run(self):
        return 1 if self.row['volS'] > self.volCoef*self.row['volL'] and self.row['close'] < self.row['bolDown'] else 0


