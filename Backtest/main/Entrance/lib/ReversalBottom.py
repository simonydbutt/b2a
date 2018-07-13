from Backtest.main.Attributes.Attr import Attr
from Backtest.main.Data.Load import Load
from Backtest.main.Visual.CandlestickChart import CandlestickChart


class ReversalBottom:

    def __init__(self, df, params):
        self.volMAPeriods = params['numPeriodsVol'] if 'numPeriodsVol' in list(params.keys()) else 100
        self.volCoef = params['volCoef'] if 'volCoef' in list(params.keys()) else 1
        self.maPeriods = params['numPeriodsMA'] if 'numPeriodsMA' in list(params.keys()) else 30
        self.numStd = params['numStd'] if 'numStd' in list(params.keys()) else 2
        self.bolCoef = params['bolCoef'] if 'bolCoef' in list(params.keys()) else 1

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
            ).add('VolNorm', params={})
        ).add('MA', params={
            'col': 'vol',
            'numPeriods': self.volMAPeriods,
            'attrName': 'volMA'
        }).iloc[max(self.volMAPeriods, self.maPeriods):]
        print(len(df))

    def run(self):
        self.df['isReversal'] = self.df.apply(self.conditions, axis=1)
        return list(self.df[self.df['isReversal'] == True]['TS'].values)

    def conditions(self, row):
        return row['vol'] > self.volCoef*row['volMA'] and row['close'] < self.bolCoef*row['bollingerDown']


# df = Load('binance').loadOne('XMRBTC_2h', '01/01/2018', timeEnd='01/06/2018')
# RB = ReversalBottom(df, params={'volCoef': 1, 'numStd': 1.5})
# CC = CandlestickChart()
# print(RB.run())
#
# for i in RB.run():
#     CC.plotStrat(df, i, i+30*2*60*60)