from Pipeline.main.Utils.ExchangeUtil import ExchangeUtil
from Pipeline.main.PullData.Price.lib._Pull import _Pull
import pandas as pd
import Settings
import logging
import hashlib
import requests
import json
import hmac
import time


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

    def makeTrade(self, asset, quantity, dir):
        t = round(time.time() * 1000)
        paramString = 'symbol=%s&timestamp=%s&side=%s&type=MARKET&quantity=%s' % (asset, t, dir.upper(), quantity)
        sig = hmac.new(msg=paramString.encode('utf-8'), key=Settings.TRADE['sec'].encode('utf-8'),
                       digestmod=hashlib.sha256).hexdigest()
        req = requests.post('%s/api/v3/order?%s' % (self.baseURL, paramString),
                            headers={'X-MBX-APIKEY': Settings.TRADE['apiKey']},
                            params={'signature': sig})
        return json.loads(req.content.decode('utf-8'))
