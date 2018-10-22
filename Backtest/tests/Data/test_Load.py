from Backtest.main.Data.Load import Load
import pandas as pd
import Settings
import os


"""
    Tests for Load function
    
    * as not prepared to set up travis mongo testing just yet, will only be for csv load
"""

L = Load("binance", dbLite=True)


def test_MakeNumeric():
    sampleRaw = pd.DataFrame(
        [["12", "10", "5"], ["10", "10", "2"]], columns=["a", "b", "c"]
    )
    sampleNum = pd.DataFrame([[12, 10, "5"], [10, 10, "2"]], columns=["a", "b", "c"])
    assert L.makeNumeric(sampleRaw, fieldList=["a", "b"]).equals(sampleNum)


def test_loadCSV():
    loc = (
        "../resources/"
        if os.getcwd() == "%s/Backtests/tests/Data/" % Settings.BASE_PATH
        else "%s/Backtest/tests/resources/" % Settings.BASE_PATH
    )
    df = L.loadCSV(file="XMRBTC_1d_11", location=loc)
    assert len(df) == 11
    assert list(df.keys()) == [
        "milliTimestamp",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "quoteVol",
        "numTrades",
        "takerBaseAssetVol",
        "takerQuoteAssetVol",
        "TS",
    ]


if __name__ == "__main__":
    test_loadCSV()
    test_MakeNumeric()
