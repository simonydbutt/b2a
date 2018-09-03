from Pipeline.main.Utils.ExchangeUtil import ExchangeUtil
from Pipeline.main.PullData.Price.lib._Pull import _Pull
import pandas as pd


class Binance(_Pull):

    def __init__(self, logger):
        _Pull.__init__(self, logger=logger)
        self.EU = ExchangeUtil()
        self.baseURL = 'https://api.binance.com'

    def getBTCAssets(self, justQuote=False):
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

    def getAssetPrice(self, symbol, dir='buy'):
        tickData = self._pullData('/api/v1/depth', params={'symbol': symbol, 'limit': 5})
        if tickData:
            if len(tickData['bids' if dir == 'sell' else 'asks']) != 0:
                return float(tickData['bids' if dir == 'sell' else 'asks'][0][0])
            else:
                print('Zero liquidity')
                return -1
        else:
            return -1
