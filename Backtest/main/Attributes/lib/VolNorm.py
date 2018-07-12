import numpy as np


class VolNorm:

    """
        Works on Binance, may not on other exchanges
    """

    def __init__(self, df, params):
        self.df = df
        self.pVol = self.df['takerQuoteAssetVol'] / self.df['takerBaseAssetVol']
        self.attrName = params['attrName'] if 'attrName' in list(params.keys()) else 'vol'

    def run(self):
        return [(self.attrName, self.pVol)]