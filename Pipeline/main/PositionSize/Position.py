from Pipeline.main.PositionSize.lib import *
import Settings
import yaml


class Position:

    def __init__(self, stratFilePath, capFileName='Capital.yml', capFilePath='Pipeline/DB'):
        with open('%s/%s' % (Settings.BASE_PATH, stratFilePath)) as stratFile:
            self.strat = yaml.load(stratFile)['positionSize']
        with open('%s/%s/%s' % (Settings.BASE_PATH, capFilePath, capFileName)) as capFile:
            self.capital = yaml.load(capFile)

    def getSize(self, asset=None):
        return eval(self.strat['name'])(stratParams=self.strat, capParams=self.capital).get(asset=asset)