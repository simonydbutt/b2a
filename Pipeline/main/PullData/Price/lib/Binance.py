from Pipeline.main.Utils.ExchangeUtil import ExchangeUtil
from Pipeline.main.PullData.Price.lib._Pull import _Pull
import pandas as pd
import logging
import time


class Binance(_Pull):
    def __init__(self, emailOnFailure=True):
        _Pull.__init__(self)
        self.EU = ExchangeUtil()
        self.baseURL = "https://api.binance.com"
        self.emailOnFailure = emailOnFailure

    def getBTCAssets(self, justQuote=False):
        logging.debug("Starting Binance.getBTCAssets")
        return [
            val["symbol"][:-3] if justQuote else val["symbol"]
            for val in self._pullData("/api/v1/exchangeInfo")["symbols"]
            if "BTC" in val["symbol"] and "USDT" not in val["symbol"]
        ]

    def getCandles(self, asset, limit, interval, columns, lastReal):
        df = pd.DataFrame(
            self._pullData(
                "/api/v1/klines",
                params={
                    "symbol": asset,
                    "limit": limit + 1,
                    "interval": self.EU.candlestickInterval(
                        interval, exchange="Binance"
                    ),
                },
            ),
            columns=self.EU.candlestickColumns(exchange="Binance"),
        )
        df = df.iloc[:-1] if lastReal else df.iloc[1:]
        df[["open", "close", "high", "low", "volume"]] = df[
            ["open", "close", "high", "low", "volume"]
        ].apply(pd.to_numeric)
        df["TS"] = df["milliTSClose"] / 1000
        return df[columns]

    def _orderBook(self, asset, limit):
        logging.debug("Starting Binance._getOrderBook")
        return self._pullData("/api/v1/depth", params={"symbol": asset, "limit": limit})

    def getAssetPrice(self, asset, dir="buy"):
        logging.debug("Starting Binnace.getAssetPrice")
        logging.debug(
            "Pulling tick data for asset: %s and direction: %s" % (asset, dir)
        )
        tickData = self._orderBook(asset=asset, limit=5)
        if tickData:
            logging.debug("Getting latest price")
            if len(tickData["bids" if dir == "sell" else "asks"]) != 0:
                logging.debug("Adequate liquidity")
                return float(tickData["bids" if dir == "sell" else "asks"][0][0])
            else:
                logging.warning("Zero liquidity for asset: %s" % asset)
                return -1
        else:
            logging.warning("_pullData errored out, returning error code: -1")
            return -1

    def makeTrade(self, asset, quantity, dir):
        logging.debug("Starting Binance.makeTrade")
        t = round(time.time() * 1000)
        paramString = "symbol=%s&timestamp=%s&side=%s&type=MARKET&quantity=%s" % (
            asset,
            t,
            dir.upper(),
            quantity,
        )
        return self._pullEncrypt(
            endPoint="api/v3/order", paramString=paramString, isGet=False
        )

    def getAccount(self):
        logging.debug("Starting Binance.getAccount")
        t = round(time.time() * 1000)
        accountVals = self._pullEncrypt(
            endPoint="api/v3/account", paramString="timestamp=%s" % t
        )
        return [
            [val["asset"], float(val["free"])]
            for val in accountVals["balances"]
            if float(val["free"]) != 0
        ]

    def getDepositStatus(self):
        logging.debug("Starting Binance.getDepositStatus")
        t = round(time.time() * 1000)
        depositVals = self._pullEncrypt(
            endPoint="wapi/v3/assetDetail.html", paramString=f"timestamp={t}"
        )["assetDetail"]
        return {val: depositVals[val]["depositStatus"] for val in depositVals.keys()}

    def getOrderBook(self, asset, limit):
        logging.debug("Starting Binance.getOrderBook")
        orderBook = self._orderBook(asset=asset, limit=limit)
        return {
            "bids": [[float(val[1]), float(val[0])] for val in orderBook["bids"]],
            "asks": [[float(val[1]), float(val[0])] for val in orderBook["asks"]],
        }

    def getTrades(self, asset, limit, maxTime):
        time = self._pullData("/api/v1/time")["serverTime"]
        trades = self._pullData(
            "/api/v1/trades", params={"symbol": asset, "limit": limit}
        )
        data = [
            [
                val["price"],
                float(val["qty"]),
                (time - val["time"]) / 1000,
                "s" if val["isBuyerMaker"] else "b",
            ]
            for val in trades
        ]
        df = (
            pd.DataFrame(data, columns=["Price", "Qty", "Timestamp", "Buy/Sell"])
            .sort_values("Timestamp")
            .reset_index(drop=True)
        )
        if maxTime:
            if df.iloc[-1]["Timestamp"] >= maxTime:
                return df[df["Timestamp"] <= maxTime]
            else:
                return []
        else:
            return df

    def getTicker(self):
        return self._pullData(endPoint="/api/v1/ticker/24hr")
