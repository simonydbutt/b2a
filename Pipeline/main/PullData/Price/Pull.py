from Pipeline.main.PullData.Price.lib import *
import logging


class Pull:

    def __init__(self, exchange):
        self.exchange = exchange

    def BTCAssets(self, justQuote=False):
        logging.debug('Starting Pull.BTCAssets')
        logging.debug('Variable: justQuote: %s' % justQuote)
        return eval(self.exchange)().getBTCAssets(justQuote=justQuote)

    def candles(self, asset, limit, interval, columns=['TS', 'open', 'high', 'low', 'close', 'takerQuoteVol'], lastReal=True):
        logging.debug('Starting Pull.candles')
        logging.debug('Variables. Asset: %s, limit: %s, interval: %s, columns: %s, lastReal: %s' %
                      (asset, limit, interval, columns, lastReal))
        return eval(self.exchange)().getCandles(asset=asset, limit=limit, interval=interval, columns=columns, lastReal=lastReal)

    def assetPrice(self, asset, dir='buy'):
        logging.debug('Starting Pull.assetPrice')
        logging.debug('Variables. Asset: %s, dir: %s' % (asset, dir))
        return eval(self.exchange)().getAssetPrice(asset, dir)
