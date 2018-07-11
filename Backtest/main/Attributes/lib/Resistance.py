import numpy as np


class Resistance:

    def __init__(self, df, params):
        self.df = df
        self.high = self.df['high']
        self.numPeriods = params['numPeriods'] if 'numPeriods' in list(params.keys()) else 12
        self.coef = params['coef'] if 'coef' in list(params.keys()) else 1
        self.attrName = params['attrName'] if 'attrName' in list(params.keys()) else 'resistance'

    def run(self):
        resList = [np.NaN for _ in range(self.numPeriods)]
        for i in range(self.numPeriods, len(self.high)):
            resList.append(self.coef * np.max(self.high[i - self.numPeriods: i]))
        return [(self.attrName, resList)]