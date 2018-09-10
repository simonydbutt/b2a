from tinydb import TinyDB
import Settings


class FundamentalRules:

    """
        The getAssets function loads a db (assetSelect.ujson) which contains the assets selected in FR.analyse

    """

    def __init__(self, config, logger):
        self.logger = logger
        self.config = config
        self.assetDB = TinyDB('%s/Pipeline/DB/%s/%s/assetSelect.ujson' \
                              % (Settings.BASE_PATH, self.config['dbName'], self.config['stratName']))

    def getAssets(self):
        return [(val['asset'], val['exchange']) for val in self.assetDB.all()]

    def analyse(self):
        pass
