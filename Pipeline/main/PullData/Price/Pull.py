from Pipeline.main.PullData.Price.lib import *


class Pull:

    def __init__(self, exchange, logger):
        self.exchange = exchange
        self.logger = logger

    def BTCAssets(self, justQuote=False):
        return eval(self.exchange)(logger=self.logger).getBTCAssets(justQuote=justQuote)

    def candles(self, asset, limit, interval, columns=['TS', 'open', 'high', 'low', 'close', 'takerQuoteVol']):
        return eval(self.exchange)(logger=self.logger).getCandles(asset=asset, limit=limit, interval=interval, columns=columns)

    def assetPrice(self, symbol, dir='buy'):
        return eval(self.exchange)(logger=self.logger).getAssetPrice(symbol, dir)
