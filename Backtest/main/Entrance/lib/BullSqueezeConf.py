from Backtest.main.Attributes.Attr import Attr


class BullSqueezeConf:

    """
        Pairs a Bull Squeeze candlestick formation with a confirming white session

        Test pairing w. isFeasible or MA
    """

    def __init__(self, df, params):
        self.coef = params['coef'] if 'coef' in params.keys() else 0.001
        self.numPeriods = params['numPeriods'] if 'numPeriods' in params.keys() else 3
        self.df = Attr(df).add('BullSqueeze', params={'numPeriods': self.numPeriods, 'coef': self.coef})

    def run(self):
        self.df['bullSqueezeConf'] = self.df.apply(self.conditions, axis=1)
        return list(self.df[self.df['bullSqueezeConf']]['TS'].values)

    def conditions(self, row):
        return False not in [row['bullSqueeze'], row['close'] > row['bullConf']]
