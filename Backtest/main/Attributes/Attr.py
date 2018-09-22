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



# df = Load('bitmex').loadOne('ETHUSD_5m', '01/06/2018', limit=10000)
# df = Attr(df).add('PivotLines', params={})
# for i in range(5):
#     print(df.iloc[-i])
