from Pipeline.main.PullData.Price.Pull import Pull
import numpy as np
import pandas as pd


class CheapVol:

    """
        Profits from buying shitcoins in accumulation phase.
        Enters when price is still cheap and volume spikes
    """

    def __init__(self, params, logger, isTest=False):
        pd.options.mode.chained_assignment = None
        self.isTest = isTest
        self.params = params['enter']
        self.pull = Pull(exchange=self.params['exchange'], logger=logger)
        self.logger = logger

    def run(self, asset, testData=None):
        self.logger.debug('Starting CheapVol for asset: %s' % asset)
        df = self.pull.candles(asset=asset, interval=self.params['granularity'],
                               limit=max(self.params['periodsVolLong'], self.params['periodsMA']),
                               columns=['close', 'takerQuoteVol'], lastReal=True) if not self.isTest else testData
        row = df.iloc[-1]
        row['volL'] = np.nanmean(df.iloc[-self.params['periodsVolLong']:]['takerQuoteVol'])
        row['volS'] = np.nanmean(df.iloc[-self.params['periodsVolShort']:]['takerQuoteVol'])
        bolData = df.iloc[-self.params['periodsMA']:]['close']
        row['bolDown'] = np.nanmean(bolData) - self.params['bolStd'] * np.nanstd(bolData)
        isEnter = row['volS'] > self.params['volCoef']*row['volL'] and row['close'] < row['bolDown']
        self.logger.debug('Entering position for asset: %s' % asset if isEnter else
                          'No action for asset: %s' % asset)
        return isEnter
