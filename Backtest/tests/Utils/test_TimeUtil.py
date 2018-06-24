from Backtest.main.Utils.TimeUtil import TimeUtil


"""
    Tests for TimeUtil class
"""

TU = TimeUtil()


def test_getTS():
    assert TU.getTS('2018-11-05T00:00:00.000Z') == 1541376000
    assert TU.getTS('06/24/2018 21:26:00', timeFormat='%m/%d/%Y %H:%M:%S') == 1529871960



