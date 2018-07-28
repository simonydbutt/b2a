from Backtest.tests.resources.TestingLoad import TestingLoad
from Backtest.main.Attributes.lib.MA import MA
import numpy as np



def test_MA():
    df = TestingLoad().df
    periods = 5
    ma = MA(df, params={
        'numPeriods': periods,
        'col': 'high'
    }).run()[0][1]
    assert False not in [np.isnan(ma[i]) for i in range(periods)]
    assert True not in [np.isnan(ma[j]) for j in range(periods, len(ma))]
    assert ma[10] == round(float(np.sum(df.high.iloc[10-periods: 10])/periods), 6)

test_MA()
