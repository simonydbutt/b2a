from Pipeline.main.AssetSelection.lib import *


class Select:

    def __init__(self, config, logger):
        self.config = config['assetSelection']
        self.logger = logger

    def assets(self):
        return eval(self.config['name'])(config=self.config, logger=self.logger).getAssets()
