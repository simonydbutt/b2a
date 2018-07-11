import numpy as np


class MA:

    def __init__(self, df, params):
        self.df = df
        self.col = self.df[params['col']] if 'col' in list(params.keys()) else self.df['close']
        self.numPeriods = params['numPeriods'] if 'numPeriods' in list(params.keys()) else 24
        self.attrName = params['attrName'] if 'attrName' in list(params.keys()) else 'ma%s' % self.numPeriods

    def run(self):
        maList = [np.NAN for _ in range(self.numPeriods)]
        for i in range(self.numPeriods, len(self.col)):
            maList.append(np.mean(self.col[i-self.numPeriods: i].values))
        return [(self.attrName, maList)]
