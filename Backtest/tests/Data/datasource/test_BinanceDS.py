from Backtest.main.Data.datasource.BinanceDS import BinanceDS


B = BinanceDS()


def test_pullCandles():
    """
        '1d' == 86400
    """
    startTime = 1514764800
    endTime = 1516406400
    df = B.pullCandles('ETHBTC', '1d', startTime=1514764800, endTime=1516406400, isDemo=True)
    assert len(df) == (endTime - startTime) / 86400 + 1
    assert list(df.keys()) == ['milliTimestamp', 'open', 'high', 'low', 'close', 'volume', 'quoteVol',
                               'numTrades', 'takerBaseAssetVol', 'takerQuoteAssetVol', 'TS']

def test_list2Dict():
    rawData = [1514764800000, '0.05358600', '0.05720000', '0.05340100', '0.05636700', '312440.75700000', 1514851199999, '17404.15888156', 406017, '150566.08800000', '8389.50328492', '0']
    dictData = {
        'milliTimestamp': 1514764800000, 'open': '0.05358600', 'high': '0.05720000', 'low': '0.05340100',
        'close': '0.05636700', 'volume': '312440.75700000', 'quoteVol': '17404.15888156', 'numTrades': 406017,
        'takerBaseAssetVol': '150566.08800000', 'takerQuoteAssetVol': '8389.50328492', 'TS': 1514764800.0
    }
    dict = B.list2Dict(rawData)
    assert False not in [dictData[val] == dict[val] for val in dictData.keys()]