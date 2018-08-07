from Backtest.main.Data.Load import Load


def testingLoad(fileName='XMRBTC_1d_11', loc=None):
    location = loc if loc else 'Backtest/tests/resources/'
    return Load('binance', dbLite=True).loadCSV(file=fileName, location=location)
