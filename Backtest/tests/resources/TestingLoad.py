from Backtest.main.Data.Load import Load


class TestingLoad:

    def __init__(self, fileName='XMRBTC_1d_11', loc=None):
        location = loc if loc else 'Backtest/tests/resources/'
        self.df = Load('binance', dbLite=True).loadCSV(file=fileName, location=location)
