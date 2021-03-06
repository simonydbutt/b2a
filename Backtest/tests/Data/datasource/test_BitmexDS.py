from Backtest.main.Data.datasource.BitmexDS import BitmexDS
import requests

"""
    Tests for BitmexDS class
"""

BDS = BitmexDS()


def test_pullData():
    assert (
        str(requests.get("https://www.bitmex.com/api/v1/instrument/active"))
        == "<Response [200]>"
    )


def test_pullCandles():
    data = BDS.pullCandles(
        asset="XBTUSD",
        binSize="1h",
        startTime="2018-05-01T00:00:00.000Z",
        endTime="2018-05-03T00:00:00.000Z",
        isDemo=True,
    )
    assert len(data) == 49


def test_getInst():
    # Hard to test as contracts often change
    # Assumption: XBTUSD and ETHM18 contracts still exist
    instList = BDS.getInst()
    assert "XBTUSD" in instList


if __name__ == "__main__":
    test_pullData()
    test_pullCandles()
    test_getInst()
