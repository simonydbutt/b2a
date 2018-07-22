from Backtest.main.Attributes.Attr import Attr


class BullHammer:

    """
        Could make cleaner

        * Not promising
    """

    def __init__(self, df, params):
        self.condList = params['condList'] if 'condList' in params.keys() else ('maBelow', 'isWhiteBlack')
        self.numPeriods = params['numPeriods'] if 'numPeriods' in params.keys() else 2
        self.maLong = params['maLong'] if 'maLong' in params.keys() else 50
        self.maShort = params['maShort'] if 'maShort' in params.keys() else 10
        self.df = Attr(
            Attr(
                Attr(
                    Attr(df).add('IsWhiteBlack', params={'whiteList': [0, 1], 'blackList': [2]})
                ).add('Hammer', params={'delay': 1})
            ).add('MA', params={'numPeriods': self.maLong, 'attrName': 'maLong'})
        ).add('MA', params={'numPeriods': self.maShort, 'attrName': 'maShort'})
        self.df['maBelow'] = self.df['maLong'] > self.df['maShort']

    def run(self):
        self.df['hammerConf'] = self.df.apply(self.conditions, axis=1)
        return list(self.df[self.df['hammerConf']]['TS'].values)

    def conditions(self, row):
        return False not in [row[val] for val in self.condList] + [row['hammer']]
