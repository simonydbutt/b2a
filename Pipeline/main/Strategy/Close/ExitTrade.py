from Pipeline.main.Utils.ExchangeUtil import ExchangeUtil
from Pipeline.main.Utils.AccountUtil import AccountUtil
from Pipeline.main.PullData.Price.Pull import Pull
from pymongo import MongoClient
import Settings
import logging
import yaml
import time


class ExitTrade:
    def __init__(self, stratName, isLive=False):
        logging.debug("Initialising ExitTrade()")
        self.isLive = isLive
        self.stratName = stratName
        db = MongoClient("localhost", 27017)[stratName]
        self.transCol = db["transactionLogs"]
        self.currentCol = db["currentPositions"]
        self.pull = Pull()
        self.capDict = None

    def initBooks(self):
        logging.debug("Starting ExitTrade.initBooks")
        with open(
            "%s/Pipeline/resources/%s/capital.yml"
            % (Settings.BASE_PATH, self.stratName)
        ) as capFile:
            self.capDict = yaml.load(capFile)
        logging.debug("Ending ExitTrade.initBooks")

    def _getPrice(self, fills):
        return round(
            sum([float(val["price"]) * float(val["qty"]) for val in fills])
            / sum([float(val["qty"]) for val in fills]),
            8,
        )

    def exit(self, positionDict, currentPrice):
        logging.debug("Starting ExitTrade.exit")
        fees = ExchangeUtil().fees(exchange=positionDict["exchange"])
        dir = positionDict["dir"] if "dir" in positionDict.keys() else "buy"
        leverage = positionDict["leverage"] if "leverage" in positionDict.keys() else 1
        exitPositionSize = (
            round(
                (currentPrice / float(positionDict["openPrice"]))
                * float(positionDict["positionSize"])
                * (1 - fees),
                6,
            )
            if dir == "buy"
            else round(
                (float(positionDict["openPrice"] / currentPrice))
                * float(positionDict["positionSize"])
                * (1 - fees),
                6,
            )
        )
        logging.debug(
            "Removing val from db.currentPosition & inserting into db.tranactionLog"
        )
        self.currentCol.delete_one({"assetName": positionDict["assetName"]})
        if not self.isLive:
            realPnL = (exitPositionSize - positionDict["positionSize"]) * leverage
            exitDict = {
                "assetName": positionDict["assetName"],
                "openPrice": round(float(positionDict["openPrice"]), 8),
                "closePrice": round(currentPrice, 8),
                "percentPnL": round(currentPrice / positionDict["openPrice"] - 1, 6),
                "TSOpen": positionDict["TSOpen"],
                "TSClose": round(time.time()),
                "periods": positionDict["periods"] + 1,
                "positionSize": positionDict["positionSize"],
                "realPnL": round(realPnL, 8),
            }
        else:
            orderDict = self.pull.makeTrade(
                exchange=positionDict["exchange"],
                asset=positionDict["assetName"],
                quantity=positionDict["posSizeBase"],
                dir="SELL",
            )
            realPnL = orderDict["cummulativeQuoteQty"] - positionDict["positionSize"]
            closePrice = self._getPrice(orderDict["fills"])
            exitDict = {
                "assetName": positionDict["assetName"],
                "openPrice": round(positionDict["openPrice"], 8),
                "hitPrice": round(positionDict["hitPrice"], 8),
                "sellPrice": round(positionDict["sellPrice"], 8),
                "closePrice": closePrice,
                "percentPnL": round(closePrice / positionDict["openPrice"] - 1, 6),
                "TSOpen": positionDict["TSOpen"],
                "TSClose": round(time.time()),
                "periods": positionDict["periods"] + 1,
                "positionSize": positionDict["positionSize"],
                "realPnL": round(realPnL, 8),
            }
        self.transCol.insert_one(exitDict)
        self.capDict["liquidCurrent"] += exitPositionSize
        logging.debug("Ending ExitTrade.run")

    def paperValue(self):
        logging.debug("Starting ExitTrade.paperValue")
        return sum([val["paperSize"] for val in list(self.currentCol.find())])

    def closeOutBooks(self):
        logging.debug("Starting ExitTrade.closeOutBooks")
        if not self.isLive:
            self.capDict["paperCurrent"] = round(
                self.capDict["liquidCurrent"] + self.paperValue(), 4
            )
            self.capDict["percentAllocated"] = round(
                1 - self.capDict["liquidCurrent"] / self.capDict["paperCurrent"], 3
            )
            self.capDict["paperPnL"] = round(
                self.capDict["paperCurrent"] / self.capDict["initialCapital"], 3
            )
            self.capDict["liquidCurrent"] = round(self.capDict["liquidCurrent"], 4)
        else:
            # **TODO hard coding 'Binance' as whole capDict system will need to change to capListDict when adding multiple
            self.capDict = AccountUtil(exchange="Binance").getValue(
                initCapital=self.capDict["initialCapital"]
            )
        with open(
            "%s/Pipeline/resources/%s/capital.yml"
            % (Settings.BASE_PATH, self.stratName),
            "w",
        ) as capFile:
            yaml.dump(self.capDict, capFile)
        logging.debug("Ending ExitTrade.closeOutBooks")
