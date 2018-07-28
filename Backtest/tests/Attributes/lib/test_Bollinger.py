from Backtest.main.Attributes.lib.Bollinger import Bollinger
from Backtest.tests.resources.TestingLoad import TestingLoad
from Backtest.main.Attributes.Attr import Attr
import numpy as np


def test_Bollinger():
    numPeriods = 5
    df = Attr(TestingLoad().df).add('MA', params={'numPeriods': numPeriods})
    maCol = df['ma%s' % numPeriods]
    bol = Bollinger(df=df, params={'numPeriods': numPeriods, 'numStd': 10}).run()
    p = 8
    assert bol[0][1][p] == round(float(df['ma%s' % numPeriods].iloc[p] + 10*np.std(df['close'].iloc[p - numPeriods: p])), 6)
    p = 5
    assert bol[1][1][p] == round(float(df['ma%s' % numPeriods].iloc[p] - 10*np.std(df['close'].iloc[p - numPeriods: p])), 6)
