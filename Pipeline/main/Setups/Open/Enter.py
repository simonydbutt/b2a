from Pipeline.main.Setups.Open.lib import *
import Settings
import yaml


class Enter:

    def __init__(self, stratName, stratPath='Pipeline/DB/Configs'):
        with open('%s/%s/%s' % (Settings.BASE_PATH, stratPath, stratName)) as stratFile:
            self.configParams = yaml.load(stratFile)

    def run(self, asset):
        eval(self.configParams['Enter']['enterName'])(self.configParams).run()
