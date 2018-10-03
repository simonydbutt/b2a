from Backtest.main.Attributes.Attr import Attr
import numpy as np


class Pivots:

    """
        maxPeriod is the period close can exist between pivot lines before reset
    """

    def __init__(self, df, params):
        self.numPeriods = params['numPeriods'] if 'numPeriods' in params.keys() else 100
        self.maxPeriod = params['maxPeriod'] if 'maxPeriod' in params.keys() else 32
        isHalves = params['isHalves'] if 'isHalves' in params.keys() else True
        self.df = Attr(Attr(df).add('MA', params={
            'col': 'volume', 'numPeriods': 100, 'attrName': 'volMA'
        })).add('PivotLines', params={'numPeriods': self.numPeriods})
        self.pivots = ['s3', 's2.5', 's2', 's1.5', 's1', 's0.5', 'p', 'r0.5', 'r1', 'r1.5', 'r2', 'r2.5', 'r3'] if \
            isHalves else ['s3', 's2', 's1', 'p', 'r1', 'r2', 'r3']

    def _whichPivot(self, row):
        if row['close'] > row[self.pivots[0]]:
            n = 1
            while row['close'] > row[self.pivots[n]]:
                n += 1
                if n == len(self.pivots):
                    return -1
            return n
        else:
            return -1

    def run(self):
        buyAt = []
        sellAt = []
        lastLower = False
        lastHigher = False
        n = 0
        recalc = True
        for i in range(self.numPeriods + 1, len(self.df)):
            row = self.df.iloc[i]
            pivotNum = pivotNum if not recalc else self._whichPivot(row)
            recalc = False if pivotNum != -1 else True
            n += 1
            if row['close'] > row[self.pivots[pivotNum]]:
                if lastHigher and row['volMA'] > row['volume']:
                    buyAt.append(row['TS'])
                n = 0
                lastLower = True
                lastHigher = False
                recalc = True
            elif row['close'] < row[self.pivots[pivotNum - 1]]:
                if lastLower and row['volMA'] > row['volume']:
                    sellAt.append(row['TS'])
                n = 0
                lastLower = False
                lastHigher = True
                recalc = True
            if n == self.maxPeriod:
                lastLower = False
                lastHigher = False
                n = 0
        return {'buy': buyAt, 'sell': sellAt}