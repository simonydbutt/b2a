import numpy as np


class MA:

    def __init__(self, df, params):
        self.df = df
        self.close = self.df['close']
        self.numPeriods = params['numPeriods'] if 'numPeriods' in list(params.keys()) else 24
        self.attrName = params['attrName'] if 'attrName' in list(params.keys()) else 'MA_%s' % self.numPeriods

    def run(self):
        maList = [np.NAN for _ in range(self.numPeriods)]
        for i in range(self.numPeriods, len(self.close)):
            maList.append(np.mean(self.close[i-self.numPeriods: i].values))
        return [(self.attrName, maList)]
