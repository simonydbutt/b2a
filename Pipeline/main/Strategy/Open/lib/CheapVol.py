import numpy as np
import pandas as pd


class CheapVol:

    """
        Profits from buying shitcoins in accumulation phase.
        Enters when price is still cheap and volume spikes
    """

    def __init__(self, params, pullData, isTest=False):
        pd.options.mode.chained_assignment = None
        self.isTest = isTest
        self.params = params['enter']
        self.pull = pullData

    def run(self, asset, testData=None):
        df = self.pull.candles(asset=asset, interval=self.params['granularity'],
                               limit=max(self.params['periodsVolLong'], self.params['periodsMA']),
                               columns=['close', 'takerQuoteVol'], lastReal=True) if not self.isTest else testData
        row = df.iloc[-1]
        row['volL'] = np.nanmean(df.iloc[-self.params['periodsVolLong']:]['takerQuoteVol'])
        row['volS'] = np.nanmean(df.iloc[-self.params['periodsVolShort']:]['takerQuoteVol'])
        bolData = df.iloc[-self.params['periodsMA']:]['close']
        row['bolDown'] = np.nanmean(bolData) - self.params['bolStd'] * np.nanstd(bolData)
        return row['volS'] > self.params['volCoef']*row['volL'] and row['close'] < row['bolDown']
