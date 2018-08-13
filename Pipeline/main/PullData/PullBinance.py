from Pipeline.main.PullData._Pull import _Pull
import pandas as pd
import time


class PullBinance(_Pull):

    """
        # TODO: add amount to getAssetPrice to get the exact price will buy at
    """

    def __init__(self):
        _Pull.__init__(self)
        self.baseUrl = 'https://api.binance.com'

    def getBTCAssets(self, justQuote=False):
        return [val['symbol'][:-3] if justQuote else val['symbol']
                for val in self._pullData('/api/v1/exchangeInfo')['symbols'] if
                'BTC' in val['symbol'] and 'USDT' not in val['symbol']]

    def getCandles(self, asset, limit, interval, columns=['TS', 'open', 'high', 'low', 'close', 'takerQuoteVol']):
        df = pd.DataFrame(
            self._pullData('/api/v1/klines', params={
                'symbol': asset,
                'limit': limit+1,
                'interval': interval
            }),
            columns=['milliTSOpen', 'open', 'high', 'low', 'close', 'volume',
                     'milliTSClose', 'quoteVol', 'numTrades', 'takerBaseVol',
                     'takerQuoteVol', 'id_']
        )
        df = df.iloc[:-1] if df.iloc[-1]['milliTSClose']/1000 - time.time() > 0 else df.iloc[1:]
        df[['open', 'close', 'high', 'low', 'takerQuoteVol']] = \
            df[['open', 'close', 'high', 'low', 'takerQuoteVol']].apply(pd.to_numeric)
        df['TS'] = df['milliTSClose'] / 1000
        return df[columns]

    def getAssetPrice(self, sym, dir='buy'):
        tickData = self._pullData('/api/v1/depth', params={'symbol': sym, 'limit': 5})
        return float(tickData['bids' if dir == 'sell' else 'asks'][0][0])
