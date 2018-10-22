from pymongo import MongoClient
import logging


class FundamentalRules:

    """
        The getAssets function loads a db (assetSelect.ujson) which contains the assets selected in FR.analyse

    """

    def __init__(self, stratName):
        logging.debug("Initialising FundatmentalRules()")
        self.assetCol = MongoClient("localhost", 27017)[stratName]["viableAssets"]

    def getAssets(self):
        return [(val["asset"], val["exchange"]) for val in list(self.assetCol.find())]

    def analyse(self):
        # **Todo create viableAssets collection
        pass
