import numpy as np


class Bollinger:

    def __init__(self, df, params):
        self.df = df
        self.C = self.df['close']
        self.attrName = params['attrName'] if 'attrName' in list(params.keys()) else 'bollinger'
        self.numPeriods = params['numPeriods'] if 'numPeriods' in list(params.keys()) else 24
        self.MAField = params['maField'] if 'maField' in list(params.keys()) else 'ma%s' % self.numPeriods
        self.numStd = params['numStd'] if 'numStd' in list(params.keys()) else 2

    def run(self):
        bollingerUp = [np.NAN for i in range(self.numPeriods)]
        bollingerDown = [np.NAN for i in range(self.numPeriods)]
        for i in range(self.numPeriods, len(self.df)):
            std = np.std(self.C.iloc[i - self.numPeriods: i].values)
            bollingerUp.append(self.df[self.MAField].iloc[i] + self.numStd * std)
            bollingerDown.append(self.df[self.MAField].iloc[i] - self.numStd * std)
        return [
            (self.attrName + 'Up', bollingerUp),
            (self.attrName + 'Down', bollingerDown)
        ]