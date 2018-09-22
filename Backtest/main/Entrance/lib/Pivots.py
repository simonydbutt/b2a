from Backtest.main.Attributes.Attr import Attr
import numpy as np


class Pivots:

    """
        maxPeriod is the period close can exist between pivot lines before reset
    """

    def __init__(self, df, params):
        self.numPeriods = params['numPeriods'] if 'numPeriods' in params.keys() else 288
        self.maxPeriod = params['maxPeriod'] if 'maxPeriod' in params.keys() else 24
        isHalves = params['isHalves'] if 'isHalves' in params.keys() else True
        self.df = Attr(df).add('PivotLines', params={'numPeriods': self.numPeriods})
        self.pivots = ['s3', 's2.5', 's2', 's1.5', 's1', 's0.5', 'p', 'r0.5', 'r1', 'r1.5', 'r2', 'r2.5', 'r3'] if \
            isHalves else ['s3', 's2', 's1', 'p', 'r1', 'r2', 'r3']

    def _whichPivot(self, price, row):
        if price < self.pivots[0]:
            n = 1
            while price > row[self.pivots[n]]:
                n += 1
                if n == len(self.pivots):
                    return -1
            return n
        else:
            return -1

    def run(self):
        enterAt = []
        for i in range(self.numPeriods, len(self.df)):
            pivotNum = self._whichPivot(price=self.df['close'], row=self.df.iloc[i])
            if pivotNum != -1:
                periodDF = self.df.iloc[i - self.maxPeriod:i]['close']
                upperPivot = self.pivots[pivotNum]
                lowerPivot = self.pivots[pivotNum - 1]
                periodDF
        return enterAt