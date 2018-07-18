import numpy as np


class MA:

    def __init__(self, df, params):
        self.df = df
        self.col = self.df[params['col']] if 'col' in params.keys() else self.df['close']
        self.numPeriods = params['numPeriods'] if 'numPeriods' in params.keys() else 24
        self.attrName = params['attrName'] if 'attrName' in params.keys() else 'ma%s' % self.numPeriods

    def run(self):
        maList = [np.NAN for _ in range(self.numPeriods)]
        for i in range(self.numPeriods, len(self.col)):
            maList.append(round(float(np.mean(self.col[i-self.numPeriods: i].values)), 6))
        return [(self.attrName, maList)]
