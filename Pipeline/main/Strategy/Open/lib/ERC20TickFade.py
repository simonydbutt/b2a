from Pipeline.main.PullData.Price.Pull import Pull
import pandas as pd
import numpy as np
import Settings
import logging
import yaml


class ERC20TickFade:

    """
        Buy ETHUSD, Sell BTCUSD when erc20tick > enterVal

        Config Requirements:
            - enterVal
            - assetList = {
                'erc20': [],
                'non': []
            }
            - maxVolCoef
    """

    def __init__(self, stratName, isTest):
        logging.debug('Initilising ERC20TickFade')
        with open('%s/Pipeline/resources/%s/config.yml' % (Settings.BASE_PATH, stratName)) as configFile:
            self.enterParams = yaml.load(configFile)['enter']
        self.coinDict = self.enterParams['assetList']
        self.isTest = isTest
        self.p = Pull()
        self.coolDown = True
        self.oldData = {'erc': pd.DataFrame([]), 'non': pd.DataFrame([])}

    def _getTick(self, type):
        logging.debug('Starting ERC20TickArb._getTick()')
        newPrices = self.p.getPriceList(coinList=self.coinDict[type])
        logging.debug('Pulled new prices for type: %s' % type)
        if len(self.oldData[type]) != 0:
            logging.debug('Calculating tick value')
            tick = sum([
                1 if val > 0 else -1 if val < 0 else 0
                for val in list(newPrices['price'] - self.oldData[type]['price'])
            ])
            logging.debug('Ending ERC20TickArb._getTick()')
            logging.debug('Tick Val: %s' % tick)
            return tick
        else:
            logging.debug('Creating old data')
            self.oldData[type] = newPrices
            logging.debug('Ending ERC20TickArb._getTick()')
            return 0

    def _isVol(self):
        """
            True if vol_1d/vol_1m < maxVolCoef
        """
        data = Pull().candles(exchange='Nomics', asset='BTC', interval='1h', columns=None, lastReal=None, limit=None)
        vol = np.nanmean(data['volume'].iloc[-24:].astype(float)) / np.nanmean(data['volume'].astype(float))
        logging.debug('Vol: %s' % vol)
        return vol < self.enterParams['maxVolCoef']

    def run(self):
        logging.debug('Starting ERC20TickFade.run()')
        logging.debug('IsCoolDown: %s' % self.coolDown)
        if self._isVol() and not self.coolDown:
            tickSum = self._getTick(type='erc') - self._getTick(type='non')
            if tickSum > self.enterParams['enterVal']:
                self.coolDown = True
                return 1
            elif tickSum < -self.enterParams['enterVal']:
                self.coolDown = True
                return -1
            else:
                return 0
        else:
            logging.debug('Creating oldData')
            self.coolDown = False
            _ = self._getTick(type='erc')
            _ = self._getTick(type='non')
