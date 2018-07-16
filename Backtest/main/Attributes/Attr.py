from Backtest.main.Attributes.lib import *
from Backtest.main.Visual.CandlestickChart import CandlestickChart
from Backtest.main.Data.Load import Load


class Attr:

    def __init__(self, df):
        self.df = df

    def add(self, metricName, fields=None, params={}):
        reqFields = self.df[fields] if fields else self.df
        attrList = eval(metricName)(df=reqFields, params=params).run()
        for attrVal in attrList:
            self.df[attrVal[0]] = attrVal[1]
        return self.df


# df = Load('binance').loadOne('NULSBTC_1h', '01/01/2018', timeEnd='01/06/2018')
# df = Attr(df).add('BullSqueeze', params={'coef': .002})
# print(df[:3])
# CandlestickChart().plotEx(df, 'bullSqueeze', num=2)