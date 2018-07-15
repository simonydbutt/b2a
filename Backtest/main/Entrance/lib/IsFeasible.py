from Backtest.main.Attributes.Attr import Attr


class IsFeasible:

    """
        Two initial indicators before any chart analysis
            - vol_MA5 > vol_MA100
            - close < bollingerDown
    """

    def __init__(self, df, params):
        self.delay = params['delay'] if 'delay' in params.keys() else 0
        self.volMALongPeriods = params['numPeriodsVolLong'] if 'numPeriodsVolLong' in params.keys() else 100
        self.volMAShortPeriods = params['numPeriodsVolShort'] if 'numPeriodsVolShort' in params.keys() else 5
        self.volCoef = params['volCoef'] if 'volCoef' in params.keys() else 1
        self.maPeriods = params['numPeriodsMA'] if 'numPeriodsMA' in params.keys() else 30
        self.numStd = params['numStd'] if 'numStd' in params.keys() else 2
        self.bolCoef = params['bolCoef'] if 'bolCoef' in params.keys() else 1
        self.df = Attr(
            Attr(
                Attr(
                    Attr(df).add('MA', params={
                        'numPeriods': self.maPeriods,
                        'attrName': 'ma'
                    })
                ).add('Bollinger', params={
                    'numPeriods': self.maPeriods,
                    'numStd': self.numStd,
                    'maField': 'ma',
                    'attrName': 'bollinger'
                })
            ).add('MA', params={
                'col': 'takerQuoteAssetVol',
                'numPeriods': self.volMALongPeriods,
                'attrName': 'volMALong'
            })
        ).add('MA', params={
            'col': 'takerQuoteAssetVol',
            'numPeriods': self.volMAShortPeriods,
            'attrName': 'volMAShort'
        }).iloc[max(self.volMALongPeriods, self.maPeriods):]

    def run(self):
        gran = self.df['TS'].iloc[1] - self.df['TS'].iloc[0]
        self.df['isReversal'] = self.df.apply(self.conditions, axis=1)
        return [val + self.delay*gran for val in list(self.df[self.df['isReversal']]['TS'].values)]


    def conditions(self, row):
        return row['volMAShort'] > self.volCoef*row['volMALong'] and row['close'] < self.bolCoef*row['bollingerDown']