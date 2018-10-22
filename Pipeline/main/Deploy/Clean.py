from pymongo import MongoClient
import Settings
import logging
import shutil
import yaml
import os


class Clean:
    def __init__(self, stratName):
        logging.debug("Initialising Clean()")
        self.path = "%s/Pipeline/resources/%s" % (Settings.BASE_PATH, stratName)
        self.stratName = stratName
        self.client = MongoClient("localhost", 27017)

    def cleanStrat(self):
        logging.debug("Starting Clean.cleanStrat")
        self.client.drop_database(self.stratName)
        shutil.rmtree(self.path)
        logging.debug("Ending Clean.CleanStrat")

    def resetStrat(self):
        logging.debug("Starting Clean.resetStrat")
        self.client.drop_database(self.stratName)
        with open("%s/capital.yml" % self.path, "r") as capFile:
            initCap = yaml.load(capFile)["initialCapital"]
        with open("%s/capital.yml" % self.path, "w") as capFile:
            yaml.dump(
                data={
                    "initialCapital": initCap,
                    "liquidCurrent": initCap,
                    "paperCurrent": initCap,
                    "paperPnL": 0,
                    "percentAllocated": 0,
                },
                stream=capFile,
            )
            capFile.close()
        logging.debug("Ending Clean.resetStrat")
