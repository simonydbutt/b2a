from Pipeline.main.PullData.Price.lib.Binance import Binance
import logging

"""
    Tests binance connection and makes sure time is in sync
    * Assumes time sync within 10 seconds is okay 
"""


def test_connection():
    PB = Binance()
    assert PB._pullData("/api/v1/ping") == {}


def test_getCandles():
    PB = Binance()
    data = PB.getCandles(
        asset="ETHBTC",
        limit=5,
        interval=86400,
        columns=["TS", "open", "high", "low", "close", "volume"],
        lastReal=True,
    )
    assert len(data) == 5
    assert list(data) == ["TS", "open", "high", "low", "close", "volume"]


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    test_connection()
    test_getCandles()
