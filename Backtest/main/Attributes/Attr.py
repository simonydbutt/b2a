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


# df = Load('poloniex').loadOne('BTCETH_1d', '01/01/2016')
# df = Attr(df).add('IsWhiteBlack', params={'blackList': [0, 1, 2, 4, 5], 'whiteList': [3]})
# print(df[-5:])
# CandlestickChart().plotEx(df, 'isWhiteBlack', num=2, volName='quoteVolume')
