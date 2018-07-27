import pandas as pd
import requests
import json



class PullBinance:

    def __init__(self):
        self.baseUrl = 'https://api.binance.com'

    def pullData(self, endPoint, params=None):
        req = requests.get(self.baseUrl + endPoint, params=params)
        if req.status_code == 200:
            return json.loads(req.content.decode('utf-8'))
        elif req.status_code == 429:
            print('rate limit hit')
            return -1
        else:
            print('Other Error')
            return -2

    def getBTCAssets(self):
        return [val['symbol'] for val in self.pullData('/api/v1/exchangeInfo')['symbols'] if
                'BTC' in val['symbol'] and 'USDT' not in val['symbol']]

    def getCandles(self, asset, limit, interval, columns=['TS', 'open', 'high', 'low', 'takerQuoteVol']):
        df = pd.DataFrame(
            self.pullData('/api/v1/klines', params={
                'symbol': asset,
                'limit': limit,
                'interval': interval
            }),
            columns=['milliTSOpen', 'open', 'high', 'low', 'close', 'volume',
                     'milliTSClose', 'quoteVol', 'numTrades', 'takerBaseVol',
                     'takerQuoteVol', 'id_']
        )
        df[['open', 'close', 'high', 'low', 'taker']] = \
            df[['open', 'close', 'high', 'low', 'takerQuoteVol']].apply(pd.to_numeric)
        df['TS'] = df['milliTSClose'] / 1000
        return df[columns]
