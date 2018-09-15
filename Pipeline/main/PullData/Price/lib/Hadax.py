from Pipeline.main.Utils.ExchangeUtil import ExchangeUtil
from Pipeline.main.PullData.Price.lib._Pull import _Pull
import pandas as pd
import logging


class Hadax(_Pull):

    def __init__(self):
        _Pull.__init__(self)
        self.EU = ExchangeUtil()
        self.baseURL = 'http://api.hadax.com'

    def getBTCAssets(self, justQuote=False):
        logging.debug('Starting Hadax.getBTCAssets')
        return [
            val['symbol'][:-3].upper() if justQuote else val['symbol'].upper()
            for val in
            self._pullData('/market/tickers')['data']
            if 'btc' == val['symbol'][-3:]
        ]

    def getAssetPrice(self, asset, dir='buy'):
        logging.debug('Starting Hadax.getAssetPrice')
        logging.debug('Pulling tick data for asset: %s and direction: %s' % (asset, dir))
        tickData = self._pullData('/market/depth', params={'symbol': asset.lower(), 'type': 'step0'})['tick']
        logging.debug('Getting latest price')
        price = tickData['bids' if dir == 'sell' else 'asks'][0][0]
        logging.debug('Latest price: %s' % price)
        return price

    def getCandles(self, asset, limit, interval, columns, lastReal):
        logging.debug('Starting Hadax.getCandles')
        response = self._pullData('/market/history/kline', params={
                'symbol': asset.lower(),
                'period': self.EU.candlestickInterval(interval, exchange='Hadax'),
                'size': limit + 1
            })
        # May need timestamp which is -> timestamp = response['ts']
        logging.debug('Creating pd dataframe and sorting data')
        df = pd.DataFrame(
            response['data'], columns=self.EU.candlestickColumns(exchange='Hadax')
        ).sort_values('TS', ascending=True)
        logging.debug('Trimming data to correct size')
        df = df.iloc[:-1] if lastReal else df.iloc[1:]
        logging.debug('Ending Hadax.getCandles')
        return df[columns]
