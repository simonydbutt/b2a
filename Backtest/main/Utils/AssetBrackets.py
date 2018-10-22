from pymongo import MongoClient, DESCENDING, ASCENDING
import numpy as np


class AssetBrackets:
    def __init__(self, exchangeName="binance"):
        self.client = MongoClient("localhost", 27017)
        self.baseDB = self.client[exchangeName]
        self.measure = "takerQuoteAssetVol" if exchangeName == "binance" else "volume"

    def getUSDTVols(self):
        return {
            asset[:-3]: np.nanmean(
                [
                    float(val[self.measure])
                    for val in list(
                        self.baseDB[asset]
                        .find({}, {self.measure: 1, "_id": 0})
                        .sort("TS", DESCENDING)
                        .limit(10)
                    )
                ]
            )
            for asset in [
                col
                for col in self.baseDB.collection_names()
                if "_1d" in col and "USDT" in col
            ]
        }

    def getBTCVols(self):
        return {
            asset[:-3]: np.nanmean(
                [
                    float(val[self.measure])
                    for val in list(
                        self.baseDB[asset]
                        .find({}, {self.measure: 1, "_id": 0})
                        .sort("TS", ASCENDING)
                        .limit(10)
                    )
                ]
            )
            for asset in [
                col
                for col in self.baseDB.collection_names()
                if "_1d" in col and "USDT" not in col
            ]
        }

    def getBrackets(self, numStd=1, base="BTC"):
        volList = self.getUSDTVols() if base == "USDT" else self.getBTCVols()
        maxVol = np.max(list(volList.values()))
        bracketDict = {
            "shit": [],
            "small": [],
            "mid": [],
            "big": [],
            "all": list(volList.keys()),
        }
        for asset in volList.keys():
            if volList[asset] > 0.3 * maxVol:
                bracketDict["big"].append(asset)
            elif volList[asset] > 0.05 * maxVol:
                bracketDict["mid"].append(asset)
            elif volList[asset] > 0.01 * maxVol:
                bracketDict["small"].append(asset)
            else:
                bracketDict["shit"].append(asset)
        return bracketDict
