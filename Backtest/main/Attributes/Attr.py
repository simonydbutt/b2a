from Backtest.main.Attributes.lib import *
from Backtest.main.Data.Load import Load


class Attr:

    def __init__(self, df):
        self.df = df

    def add(self, metricName, fields=None, params=None):
        reqFields = self.df[fields] if fields else self.df
        attrVals = eval(metricName)(df=reqFields, params=params).run()
        self.df[attrVals[0]] = attrVals[1]
        return self.df


df = Load('binance').loadOne('ETHBTC_1d', '01/01/2018', limit=25)
print(Attr(df).add('DownTrend', fields=['high', 'low'], params={'numPeriods': 2}))
