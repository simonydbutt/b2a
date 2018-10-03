from Pipeline.main.PullData.Price.lib._Pull import _Pull
import pandas as pd
import Settings
import logging


class Nomics(_Pull):

    """
        First impressions, Nomics is impressive
    """

    def __init__(self):
        logging.debug('Initialising Nomics()')
        _Pull.__init__(self)
        self.baseURL = 'https://api.nomics.com/v1/'

    def priceList(self, coinList):
        logging.debug('Starting Nomics.priceList')
        priceData = [val for val in self._pullData('prices', params={'key': Settings.NOMICS['apiKey']}) if
                     val['currency'] in coinList] if coinList \
            else self._pullData('prices', params={'key': Settings.NOMICS['apiKey']})
        return pd.DataFrame([
            {
                'coin': val['currency'],
                'price': float(val['price'])
            } for val in priceData
        ])

    def getCandles(self, asset, limit, interval, columns, lastReal):
        logging.debug('Starting Nomics.getCandles')
        return pd.DataFrame(
            self._pullData(
                'candles',
                params={'currency': asset, 'interval': interval, 'key': Settings.NOMICS['apiKey']}
        ))