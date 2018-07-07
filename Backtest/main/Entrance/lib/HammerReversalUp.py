from Backtest.main.Attributes.Attr import Attr


class HammerReversalUp:

    def __init__(self, df, params):
        self.trendNumPeriods = params['trendNumPeriods'] if 'trendNumPeriods' in list(params.keys()) else 5
        self.trendCoef = params['trendCoef'] if 'trendCoef' in list(params.keys()) else 1
        self.trendDelay = params['tredDelay'] if 'trendDelay' in list(params.keys()) else 1
        self.hammerDir = params['hammerDir'] if 'hammerDir' in list(params.keys()) else 'None'
        self.hammerCoef = params['hammerCoef'] if 'hammerCoef' in list(params.keys()) else 5

        self.df = Attr(
            Attr(df).add(
                metricName='Hammer',
                params={'coef': self.hammerCoef, 'dir': self.hammerDir, 'attrName': 'isHammer'})
        ).add(
            metricName='TrendDown',
            params={'numPeriods': self.trendNumPeriods, 'coef': self.trendCoef, 'attrName': 'wasTrend', 'delay':self.trendDelay}
        )

    def run(self):
        self.df['isEnter'] = self.df['isHammer'] and self.df['wasTrend']
        return self.df[['TS', 'isEnter']]