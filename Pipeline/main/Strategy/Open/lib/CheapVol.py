import numpy as np
import pandas as pd
import logging


class CheapVol:

    """
        Profits from buying shitcoins in accumulation phase.
        Enters when price is still cheap and volume spikes

        Config Requirements:
            - periodsMA
            - periodsVolLong
            - periodsVolShort
            - volCoef
            - bolStd
    """

    def __init__(self, params, isTest=False):
        pd.options.mode.chained_assignment = None
        self.isTest = isTest
        self.params = params['enter']

    def run(self, asset, Pull, testData=None):
        logging.debug('Starting CheapVol.run')
        maxPeriods = max(self.params['periodsVolLong'], self.params['periodsMA'])
        logging.debug('max periods: %s' % maxPeriods)
        df = Pull.candles(asset=asset, interval=self.params['granularity'], limit=maxPeriods,
                          columns=['close', 'takerQuoteVol'], lastReal=True) if not self.isTest else testData

        if len(df) == maxPeriods:
            row = df.iloc[-1]
            row['volL'] = round(float(np.nanmean(df.iloc[-self.params['periodsVolLong']:]['takerQuoteVol'])), 5)
            row['volS'] = round(float(np.nanmean(df.iloc[-self.params['periodsVolShort']:]['takerQuoteVol'])), 5)
            bolData = df.iloc[-self.params['periodsMA']:]['close']
            row['bolDown'] = np.nanmean(bolData) - self.params['bolStd'] * np.nanstd(bolData)
            logging.debug('volL: %s, volS: %s, price: %s, bolDown: %s' %
                          (row['volL'], row['volS'], row['close'], row['bolDown']))
            return row['volS'] > self.params['volCoef']*row['volL'] and row['close'] < row['bolDown']
        else:
            logging.warning('Data is incomplete')
            return False