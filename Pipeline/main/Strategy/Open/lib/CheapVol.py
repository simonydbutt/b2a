import numpy as np
import pandas as pd
import Settings
import logging
import yaml


class CheapVol:

    """
        Profits from buying shitcoins in accumulation phase.
        Enters when price is still cheap§ and volume spikes

        Config Requirements:
            - periodsMA
            - periodsVolLong
            - periodsVolShort
            - volCoef
            - bolStd
    """

    def __init__(self, stratName, isTest=False):
        pd.options.mode.chained_assignment = None
        self.isTest = isTest
        with open('%s/Pipeline/resources/%s/config.yml' % (Settings.BASE_PATH, stratName)) as configFile:
            self.enterParams = yaml.load(configFile)['enter']

    def run(self, asset, Pull, testData=None):
        logging.debug('Starting CheapVol.run')
        maxPeriods = max(self.enterParams['periodsVolLong'], self.enterParams['periodsMA'])
        logging.debug('max periods: %s' % maxPeriods)
        df = Pull.candles(asset=asset, interval=self.enterParams['granularity'], limit=maxPeriods,
                          columns=['close', 'takerQuoteVol'], lastReal=True) if not self.isTest else testData

        if len(df) == maxPeriods:
            row = df.iloc[-1]
            row['volL'] = round(float(np.nanmean(df.iloc[-self.enterParams['periodsVolLong']:]['takerQuoteVol'])), 5)
            row['volS'] = round(float(np.nanmean(df.iloc[-self.enterParams['periodsVolShort']:]['takerQuoteVol'])), 5)
            bolData = df.iloc[-self.enterParams['periodsMA']:]['close']
            row['bolDown'] = np.nanmean(bolData) - self.enterParams['bolStd'] * np.nanstd(bolData)
            logging.debug('volL: %s, volS: %s, price: %s, bolDown: %s' %
                          (row['volL'], row['volS'], row['close'], row['bolDown']))
            return row['volS'] > self.enterParams['volCoef']*row['volL'] and row['close'] < row['bolDown']
        else:
            logging.warning('Data is incomplete')
            return False