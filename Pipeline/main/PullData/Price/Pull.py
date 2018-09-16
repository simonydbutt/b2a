from Pipeline.main.PullData.Price.lib import *
import logging


class Pull:

    def __init__(self):
        logging.debug('Initialising Pull(')

    def BTCAssets(self, exchange, justQuote=False):
        logging.debug('Starting Pull.BTCAssets')
        logging.debug('Variable: justQuote: %s' % justQuote)
        return eval(exchange)().getBTCAssets(justQuote=justQuote)

    def candles(self, exchange, asset, limit, interval, columns=('TS', 'open', 'high', 'low', 'close', 'takerQuoteVol'), lastReal=True):
        logging.debug('Starting Pull.candles')
        logging.debug('Variables. Asset: %s, limit: %s, interval: %s, columns: %s, lastReal: %s' %
                      (asset, limit, interval, columns, lastReal))
        return eval(exchange)().getCandles(asset=asset, limit=limit, interval=interval, columns=columns, lastReal=lastReal)

    def assetPrice(self, exchange, asset, dir='buy'):
        logging.debug('Starting Pull.assetPrice')
        logging.debug('Variables. Asset: %s, dir: %s' % (asset, dir))
        return eval(exchange)().getAssetPrice(asset, dir)

    def makeTrade(self, exchange, asset, quantity, dir):
        logging.debug('Starting Pull.makeTrade')
        logging.debug('Variables. Asset: %s, dir: %s, quantity: %s, exchange: %s' % \
                      (asset, dir, quantity, exchange))
