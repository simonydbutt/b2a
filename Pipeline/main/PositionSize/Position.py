from Pipeline.main.PositionSize.lib import *
import Settings
import yaml


class Position:

    def __init__(self, stratConfig, capConfig):
        self.stratConfig = stratConfig
        self.capConfig = capConfig

    def getSize(self, asset=None):
        return eval(self.stratConfig['positionSize']['name'])(stratParams=self.stratConfig['positionSize'],
                                                              capParams=self.capConfig).get(asset=asset)
