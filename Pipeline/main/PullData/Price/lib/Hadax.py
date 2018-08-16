from Pipeline.main.PullData.Price.lib._Pull import _Pull
import pandas as pd


class Hadax(_Pull):

    def __init__(self, logger):
        _Pull.__init__(self, logger=logger)
        self.baseUrl = 'http://api.hadax.com'

    def getBTCAssets(self, justQuote=False):
        return [
            val['symbol'][:-3].upper() if justQuote else val['symbol'].upper()
            for val in
            self._pullData('/market/tickers')['data']
            if 'btc' == val['symbol'][-3:]
        ]

    def getAssetPrice(self, sym, dir='buy'):
        tickData = self._pullData('/market/depth', params={'symbol': sym.lower(), 'type': 'step0'})['tick']
        return tickData['bids' if dir == 'sell' else 'asks'][0][0]

    def getCandles(self, asset, limit, interval, columns, lastReal):
        response = self._pullData('market/history/kline', params={
                'symbol': asset,
                'period': interval,
                'size': limit + 1
            })
        # May need timestamp which is -> timestamp = response['ts']
        df = pd.DataFrame(
            response['data'], columns=['TS', 'open', 'close', 'low', 'high', 'amount', 'vol', 'count']
        ).sort_values('TS', ascending=True)
        return df.iloc[:-1] if lastReal else df.iloc[1:]
