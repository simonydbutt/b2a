from Backtest.main.Attributes.Attr import Attr


class OutsideUp:

    """
        Pairs a outsideUp candlestick formation with a confirming white session
        numPeriods > 2 then -> squeeze

        * Not promising atm
    """

    def __init__(self, df, params):
        self.condList = params['condList'] if 'condList' in params.keys() else ('maBelow', 'conf')
        self.maLong = params['maLong'] if 'maLong' in params.keys() else 50
        self.maShort = params['maShort'] if 'maShort' in params.keys() else 10
        self.df = Attr(
            Attr(
                Attr(df).add('OutsideUp', params={'delay': 1})
            ).add('MA', params={'numPeriods': self.maLong, 'attrName': 'maLong'})
        ).add('MA', params={'numPeriods': self.maShort, 'attrName': 'maShort'})
        self.df['maBelow'] = self.df['maLong'] > self.df['maShort']
        self.df['conf'] = self.df['close'] > self.df['bullConf']

    def run(self):
        self.df['outsideUpConf'] = self.df.apply(self.conditions, axis=1)
        return list(self.df[self.df['outsideUpConf']]['TS'].values)

    def conditions(self, row):
        return False not in [row[val] for val in self.condList] + [row['outsideUp']]
