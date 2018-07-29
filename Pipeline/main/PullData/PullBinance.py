import pandas as pd
import requests
import json
import logging
import time


class PullBinance:

    def __init__(self):
        self.baseUrl = 'https://api.binance.com'

    def _pullData(self, endPoint, params=None):
        req = requests.get(self.baseUrl + endPoint, params=params)
        if req.status_code == 200:
            return json.loads(req.content.decode('utf-8'))
        elif req.status_code == 429:
            logging.warning('binance rate limit hit, 30 second sleep')
            time.sleep(30)
            req = requests.get(self.baseUrl + endPoint, params=params)
            if req.status_code == 429:
                logging.error('Rate limit error after timeout')
            else:
                logging.info('Rate limit back to normal')
                return json.loads(req.content.decode('utf-8'))
        else:
            logging.error('pullData requests error with error code %s' % req.status_code)

    def getBTCAssets(self):
        return [val['symbol'] for val in self._pullData('/api/v1/exchangeInfo')['symbols'] if
                'BTC' in val['symbol'] and 'USDT' not in val['symbol']]

    def getCandles(self, asset, limit, interval, columns=['TS', 'open', 'high', 'low', 'close', 'takerQuoteVol']):
        df = pd.DataFrame(
            self._pullData('/api/v1/klines', params={
                'symbol': asset,
                'limit': limit,
                'interval': interval
            }),
            columns=['milliTSOpen', 'open', 'high', 'low', 'close', 'volume',
                     'milliTSClose', 'quoteVol', 'numTrades', 'takerBaseVol',
                     'takerQuoteVol', 'id_']
        )
        df[['open', 'close', 'high', 'low', 'takerQuoteVol']] = \
            df[['open', 'close', 'high', 'low', 'takerQuoteVol']].apply(pd.to_numeric)
        df['TS'] = df['milliTSClose'] / 1000
        return df[columns]
