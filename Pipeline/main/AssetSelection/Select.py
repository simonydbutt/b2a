from Pipeline.main.AssetSelection.lib import *
import logging


class Select:

    def __init__(self, config):
        self.config = config

    def assets(self):
        logging.debug('Starting Select.assets')
        return eval(self.config['assetSelection']['name'])(config=self.config).getAssets()
