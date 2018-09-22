import numpy as np


class PivotLines:

    def __init__(self, df, params):
        """
            numperiod default 288 as testing on 5min and 288 = 12 * 24 5 min periods in a day
        """
        self.df = df
        self.numPeriods = params['numPeriods'] if 'numPeriods' in params.keys() else 288

    def run(self):
        self.df['dailyHigh'] = [np.nanmax(self.df['high'].iloc[i - self.numPeriods: i]) if i > self.numPeriods else None
                                for i in range(len(self.df))]
        self.df['dailyLow'] = [np.nanmin(self.df['low'].iloc[i - self.numPeriods: i]) if i > self.numPeriods else None
                               for i in range(len(self.df))]
        self.df['p'] = (self.df['dailyHigh'] + self.df['dailyLow'] + self.df['close'])/3
        self.df['tmpDiff'] = self.df['dailyHigh'] - self.df['dailyLow']
        self.df['r1'] = 2 * self.df['p'] - self.df['dailyLow']
        self.df['r2'] = self.df['p'] + self.df['tmpDiff']
        self.df['r3'] = self.df['r1'] + self.df['tmpDiff']
        self.df['s1'] = 2 * self.df['p'] - self.df['dailyHigh']
        self.df['s2'] = self.df['p'] - self.df['tmpDiff']
        self.df['s3'] = self.df['s1'] - self.df['tmpDiff']
        return [
            ('p', self.df['p']), ('r0.5', (self.df['p'] + self.df['r1'])/2), ('r1', self.df['r1']),
            ('r1.5', (self.df['r1'] + self.df['r2'])/2), ('r2', self.df['r2']),
            ('r2.5', (self.df['r2'] + self.df['r3'])/2), ('r3', self.df['r3']),
            ('s0.5', (self.df['p'] + self.df['s1'])/2), ('s1', self.df['s1']),
            ('s1.5', (self.df['s1'] + self.df['s2'])/2), ('s2', self.df['s2']),
            ('s2.5', (self.df['s2'] + self.df['s3'])/2), ('s3', self.df['s3'])
        ]