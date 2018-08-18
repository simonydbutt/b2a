from Pipeline.main.Setups.Open.lib import *
import Settings
import yaml


class Enter:

    def __init__(self, stratName, logger, stratPath='Pipeline/DB/Configs', isTest=False):
        with open('%s/%s/%s.yml' % (Settings.BASE_PATH, stratPath, stratName)) as stratFile:
            self.configParams = yaml.load(stratFile)
        self.strat = eval(self.configParams['enter']['name'])(params=self.configParams, logger=logger, isTest=isTest)

    def run(self, asset, testData=None):
        return self.strat.run(asset=asset, testData=testData)
