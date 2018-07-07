import numpy as np


class VolNormMA:

    """
        Works on Binance, may not on other exchanges
    """

    def __init__(self, df, params):
        self.df = df
        self.pVol = self.df['takerQuoteAssetVol'] / self.df['takerBaseAssetVol']
        self.numPeriods = params['numPeriods'] if 'numPeriods' in list(params.keys()) else 24
        self.attrName = params['attrName'] if 'attrName' in list(params.keys()) else 'volMA_%s' % self.numPeriods

    def run(self):
        return [(self.attrName, self.pVol)]