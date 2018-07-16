import numpy as np


class BullSqueeze:

    def __init__(self, df, params):
        self.df = df
        self.coef = params['coef'] if 'coef' in params.keys() else 0.001
        self.numPeriods = params['numPeriods'] if 'numPeriods' in params.keys() else 3
        self.delay = params['delay'] if 'delay' in params.keys() else 0
        self.attrName = params['attrName'] if 'attrName' in params.keys() else 'bullSqueeze'
        self.bullConfirm = params['bullConf'] if 'bullConf' in params.keys() else True

    def isWhite(self, row):
        return row['close'] > row['open']

    def run(self):
        bsList = [False for _ in range(len(self.df))]
        initMax = [np.NaN for _ in range(self.numPeriods + self.delay)]
        for i_ in range(self.numPeriods + self.delay, len(self.df)):
            i = i_ - self.delay
            if not self.isWhite(self.df.iloc[i-self.numPeriods]):
                maxVal = self.df.iloc[i-self.numPeriods]['open'] * (1-self.coef)
                initMax.append(maxVal)
                minVal = self.df.iloc[i-self.numPeriods]['close'] * (1+self.coef)
                j = self.numPeriods - 1
                while j > 0:
                    openClose = self.df.iloc[i-j][['open', 'close']]
                    if max(openClose) < maxVal and min(openClose) > minVal:
                        maxVal = max(openClose)
                        minVal = min(openClose)
                    else:
                        break
                    if j == 1:
                        bsList[i_] = True
                    j -= 1
            else:
                initMax.append(np.NaN)
        if not self.bullConfirm:
            return (self.attrName, bsList)
        else:
            return [(self.attrName, bsList), ('bullConf', initMax)]