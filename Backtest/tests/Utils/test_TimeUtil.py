from Backtest.main.Utils.TimeUtil import TimeUtil


"""
    Tests for TimeUtil class
"""

TU = TimeUtil()


def test_getTS():
    assert TU.getTS('2012-08-29 11:38:22', timeFormat='%Y-%m-%d %H:%M:%S') == 1346236702
    assert TU.getTS('2018-11-05T00:00:00.000Z') == 1541376000



