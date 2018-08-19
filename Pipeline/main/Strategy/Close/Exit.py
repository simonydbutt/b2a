from tinydb import TinyDB
import Settings
import yaml


class Exit:

    """
        If ass
    """

    def __init__(self, stratName, logger, dbPath='Pipeline/DB', isTest=False):
        with open('%s/%s/Configs/%s.yml' % (Settings.BASE_PATH, dbPath, stratName)) as stratFile:
            self.configParams = yaml.load(stratFile)
        db = TinyDB()
