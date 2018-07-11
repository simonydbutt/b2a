import numpy as np


class Support:

    def __init__(self, df, params):
        self.df = df
        self.low = self.df['low']
        self.numPeriods = params['numPeriods'] if 'numPeriods' in list(params.keys()) else 12
        self.coef = params['coef'] if 'coef' in list(params.keys()) else 1
        self.attrName = params['attrName'] if 'attrName' in list(params.keys()) else 'support'

    def run(self):
        supportList = [np.NaN for _ in range(self.numPeriods)]
        for i in range(self.numPeriods, len(self.low)):
            supportList.append(self.coef * np.min(self.low[i - self.numPeriods: i]))
        return [(self.attrName, supportList)]