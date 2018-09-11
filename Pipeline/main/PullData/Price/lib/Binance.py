from Pipeline.main.Utils.ExchangeUtil import ExchangeUtil
from Pipeline.main.PullData.Price.lib._Pull import _Pull
import logging
import pandas as pd


class Binance(_Pull):

    def __init__(self):
        _Pull.__init__(self)
        self.EU = ExchangeUtil()
        self.baseURL = 'https://api.binance.com'

    def getBTCAssets(self, justQuote=False):
        logging.debug('Starting Binance.getBTCAssets')
        return [val['symbol'][:-3] if justQuote else val['symbol']
                for val in self._pullData('/api/v1/exchangeInfo')['symbols'] if
                'BTC' in val['symbol'] and 'USDT' not in val['symbol']]

    def getCandles(self, asset, limit, interval, columns, lastReal):
        df = pd.DataFrame(
            self._pullData('/api/v1/klines', params={
                'symbol': asset,
                'limit': limit+1,
                'interval': self.EU.candlestickInterval(interval, exchange='Binance')
            }),
            columns=self.EU.candlestickColumns(exchange='Binance')
        )
        df = df.iloc[:-1] if lastReal else df.iloc[1:]
        df[['open', 'close', 'high', 'low', 'takerQuoteVol']] = \
            df[['open', 'close', 'high', 'low', 'takerQuoteVol']].apply(pd.to_numeric)
        df['TS'] = df['milliTSClose'] / 1000
        return df[columns]

    def getAssetPrice(self, asset, dir='buy'):
        logging.debug('Starting Binnace.getAssetPrice')
        logging.debug('Pulling tick data for asset: %s and direction: %s' % (asset, dir))
        tickData = self._pullData('/api/v1/depth', params={'symbol': asset, 'limit': 5})
        if tickData:
            logging.debug('Getting latest price')
            if len(tickData['bids' if dir == 'sell' else 'asks']) != 0:
                logging.debug('Adequate liquidity')
                return float(tickData['bids' if dir == 'sell' else 'asks'][0][0])
            else:
                logging.warning('Zero liquidity for asset: %s' % asset)
                return -1
        else:
            logging.warning('_pullData errored out, returning error code: -1')
            return -1
