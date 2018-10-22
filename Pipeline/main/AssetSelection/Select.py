from Pipeline.main.AssetSelection.lib import *
import Settings
import logging
import yaml


class Select:
    def __init__(self, stratName):
        with open(
            "%s/Pipeline/resources/%s/config.yml" % (Settings.BASE_PATH, stratName)
        ) as configFile:
            self.config = yaml.load(configFile)

    def assets(self):
        logging.debug("Starting Select.assets")
        return eval(self.config["assetSelection"]["name"])(
            config=self.config
        ).getAssets()
