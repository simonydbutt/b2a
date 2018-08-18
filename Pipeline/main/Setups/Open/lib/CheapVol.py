import Settings
import yaml
import numpy as np


class CheapVol:

    def __init__(self, configParams):
        self.configParams =

    def run(self):
        return self.row['volS'] > self.volCoef * self.row['volL'] and self.row['close'] < self.row['bolDown']
