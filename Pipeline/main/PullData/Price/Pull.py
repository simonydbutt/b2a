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
        return eval(exchange)().makeTrade(asset=asset, quantity=quantity, dir=dir)

    def getAccount(self, exchange):
        """
            In format: { coin1: val1, coin2: val2 }
        """
        logging.debug('Starting Pull.getAccount()')
        accountList = eval(exchange)().getAccount()
        return {val[0]: val[1] for val in accountList}

    def getTrades(self, exchange, asset, limit, maxTime=None):
        """
            In format:
                pandas df
                    Price  |  Qty  |  Timestamp  |  Buy/Sell
        """
        logging.debug('Starting Pull.getTrades')
        return eval(exchange)().getTrades(asset=asset, limit=limit, maxTime=maxTime)

    def getOrderBook(self, exchange, asset, limit):
        """
            In format:
                {
                    'bids': [[bid1, qty1], [bid2, qty2]]
                    'asks': [[ask1, qty1], [ask2, qty2]]
                }
            limit can be: 5, 10, 20, 50, 100, 500, 1000
        """
        logging.debug('Starting Pull.getOrderBook')
        return eval(exchange)().getOrderBook(asset=asset, limit=limit)
