from Pipeline.main.PositionSize.lib import *
import Settings
import logging
import yaml


class Position:
    def __init__(self, stratName):
        logging.debug("Initialising Position()")
        resPath = "%s/Pipeline/resources/%s" % (Settings.BASE_PATH, stratName)
        with open("%s/config.yml" % resPath) as configFile:
            self.stratConfig = yaml.load(configFile)
        with open("%s/capital.yml" % resPath) as capFile:
            self.capital = yaml.load(capFile)

    def getSize(self, asset=None):
        logging.debug("Starting Position.getSize")
        logging.debug("Name: %s" % self.stratConfig["positionSize"]["name"])
        return round(
            eval(self.stratConfig["positionSize"]["name"])(
                stratParams=self.stratConfig["positionSize"], capParams=self.capital
            ).get(asset=asset),
            8,
        )
