import numpy as np


class StdExit:

    """
        Take loss when close < close0 - std_t20
        Take profit when close > close0 + 2 std_t20
        Else close t = 10
    """

    def __init__(self, df, params, enterList):
        self.df = df
        self.enterList = enterList
        self.minCoef = params['minCoef'] if 'minCoef' in params.keys() else 0.5
        self.numPeriods = params['numPeriods'] if 'numPeriods' in params.keys() else 50
        self.closeAt = params['closeAt'] if 'closeAt' in params.keys() else 15
        self.stdList = params['stdDict'] if 'stdDict' in params.keys() else {'up': 2, 'down': 1}
        self.maxRun = params['maxRun'] if 'maxRun' in params.keys() else False

    def getIndex(self, df, TSVal):
        return df.index[df['TS'] == TSVal].tolist()[0]

    def run(self):
        positionList = []
        for val in self.enterList:
            pos = self.getIndex(self.df, val)
            std = np.std(self.df.iloc[max(0, pos-self.numPeriods): pos]['close'])
            enterVal = self.df.iloc[pos]['close']
            maxVal = enterVal + std*self.stdList['up']
            minVal = max(enterVal - std*self.stdList['down'], self.minCoef*enterVal)
            periods = 1
            while periods < self.closeAt and pos + periods < len(self.df):
                close = self.df.iloc[pos + periods]['close']
                if close > maxVal:
                    if self.maxRun:
                        minVal = maxVal - std*self.stdList['down']
                        maxVal += std*self.stdList['up']
                        periods += 1
                    else:
                        break
                elif close < minVal:
                    break
                else:
                    periods += 1
            positionList.append((pos, pos + periods))
        return positionList