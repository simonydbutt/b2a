from Pipeline.main.PositionSize.lib import *
import Settings
import yaml


class Position:

    def __init__(self, stratFilePath, capFilePath='Pipeline/DB/Capital.yml'):
        with open('%s/%s' % (Settings.BASE_PATH, stratFilePath)) as stratFile:
            self.strat = yaml.load(stratFile)['positionSize']
        with open('%s/%s' % (Settings.BASE_PATH, capFilePath)) as capFile:
            self.capital = yaml.load(capFile)
        print(self.capital)

    def getSize(self, asset=None):
        return eval(self.strat['name'])(stratParams=self.strat, capParams=self.capital).get(asset=asset)