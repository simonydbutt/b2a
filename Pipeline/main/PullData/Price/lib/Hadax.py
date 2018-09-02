from Pipeline.main.Utils.ExchangeUtil import ExchangeUtil
from Pipeline.main.PullData.Price.lib._Pull import _Pull
import pandas as pd


class Hadax(_Pull):

    def __init__(self, logger):
        _Pull.__init__(self, logger=logger)
        self.EU = ExchangeUtil()
        self.baseURL = 'http://api.hadax.com'

    def getBTCAssets(self, justQuote=False):
        return [
            val['symbol'][:-3].upper() if justQuote else val['symbol'].upper()
            for val in
            self._pullData('/market/tickers')['data']
            if 'btc' == val['symbol'][-3:]
        ]

    def getAssetPrice(self, symbol, dir='buy'):
        tickData = self._pullData('/market/depth', params={'symbol': symbol.lower(), 'type': 'step0'})['tick']
        return tickData['bids' if dir == 'sell' else 'asks'][0][0]

    def getCandles(self, asset, limit, interval, columns, lastReal):
        response = self._pullData('/market/history/kline', params={
                'symbol': asset.lower(),
                'period': self.EU.candlestickInterval(interval, exchange='Hadax'),
                'size': limit + 1
            })
        # May need timestamp which is -> timestamp = response['ts']
        df = pd.DataFrame(
            response['data'], columns=self.EU.candlestickColumns(exchange='Hadax')
        ).sort_values('TS', ascending=True)
        df = df.iloc[:-1] if lastReal else df.iloc[1:]
        return df[columns]