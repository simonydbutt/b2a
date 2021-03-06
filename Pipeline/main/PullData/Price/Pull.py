from Pipeline.main.PullData.Price.lib import *
import logging


class Pull:

    """
        *TODO lots of functions, see if any are unnecessary
    """

    def __init__(self, emailOnFailure=True):
        logging.debug("Initialising Pull()")
        self.emailOnFailure = emailOnFailure

    def BTCAssets(self, exchange, justQuote=False, exchange_=None):
        logging.debug("Starting Pull.BTCAssets")
        logging.debug("Variable: justQuote: %s" % justQuote)
        if exchange == "Nomics":
            return eval(exchange)(emailOnFailure=self.emailOnFailure).getBTCAssets(
                justQuote=justQuote, exchange=exchange_
            )
        else:
            return eval(exchange)(emailOnFailure=self.emailOnFailure).getBTCAssets(
                justQuote=justQuote
            )

    def candles(
        self,
        exchange,
        asset,
        limit,
        interval,
        columns=["TS", "open", "high", "low", "close", "volume"],
        lastReal=True,
    ):
        logging.debug("Starting Pull.candles")
        logging.debug(
            "Variables. Asset: %s, limit: %s, interval: %s, columns: %s, lastReal: %s"
            % (asset, limit, interval, columns, lastReal)
        )
        return eval(exchange)(emailOnFailure=self.emailOnFailure).getCandles(
            asset=asset,
            limit=limit,
            interval=interval,
            columns=columns,
            lastReal=lastReal,
        )

    def assetPrice(self, exchange, asset, dir="buy"):
        logging.debug("Starting Pull.assetPrice")
        logging.debug("Variables. Asset: %s, dir: %s" % (asset, dir))
        return eval(exchange)(emailOnFailure=self.emailOnFailure).getAssetPrice(
            asset, dir
        )

    def makeTrade(self, exchange, asset, quantity, dir):
        logging.debug("Starting Pull.makeTrade")
        logging.debug(
            "Variables. Asset: %s, dir: %s, quantity: %s, exchange: %s"
            % (asset, dir, quantity, exchange)
        )
        return eval(exchange)(emailOnFailure=self.emailOnFailure).makeTrade(
            asset=asset, quantity=quantity, dir=dir
        )

    def getAccount(self, exchange):
        """
            In format: { coin1: val1, coin2: val2 }
        """
        logging.debug("Starting Pull.getAccount()")
        accountList = eval(exchange)(emailOnFailure=self.emailOnFailure).getAccount()
        return {val[0]: val[1] for val in accountList}

    def getTrades(self, exchange, asset, limit, maxTime=None):
        """
            In format:
                pandas df
                    Price  |  Qty  |  Timestamp  |  Buy/Sell
        """
        logging.debug("Starting Pull.getTrades")
        return eval(exchange)(emailOnFailure=self.emailOnFailure).getTrades(
            asset=asset, limit=limit, maxTime=maxTime
        )

    def getOrderBook(self, exchange, asset, limit):
        """
            In format:
                {
                    'bids': [[bid1, qty1], [bid2, qty2]]
                    'asks': [[ask1, qty1], [ask2, qty2]]
                }
            limit can be: 5, 10, 20, 50, 100, 500, 1000
        """
        logging.debug("Starting Pull.getOrderBook")
        return eval(exchange)(emailOnFailure=self.emailOnFailure).getOrderBook(
            asset=asset, limit=limit
        )

    def getTickerStats(self, exchange):
        logging.debug("Starting Pull.getTicker")
        return eval(exchange)(emailOnFailure=self.emailOnFailure).getTicker()

    def getPriceList(self, coinList=None):
        logging.debug("Starting Pull.getPriceList")
        return Nomics(emailOnFailure=self.emailOnFailure).priceList(coinList=coinList)

    def getPriceAction(self, exchange, startDate, baseAsset="BTC"):
        """
            In format:
                {
                    'asset': {'price': , 'vol': }
                }
        """
        logging.debug("Starting Pull.getPriceAction")
        return Nomics(emailOnFailure=self.emailOnFailure).getIntervalPriceAction(
            exchange, startDate, baseAsset
        )

    def getDepositStatus(self, exchange):
        """
            In format
                {
                    'asset': isDelisted (True/False)
                }
        """
        logging.debug("Starting Pull.getDepositStatus")
        return eval(exchange)(emailOnFailure=self.emailOnFailure).getDepositStatus()
