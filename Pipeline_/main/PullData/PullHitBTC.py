from Pipeline_.main.PullData._Pull import _Pull


class PullHitBTC(_Pull):

    """
        Initially using for CommitValue
    """

    def __init__(self):
        _Pull.__init__(self)
        self.baseUrl = 'https://api.hitbtc.com/api/2'

    def getBTCAssets(self, justQuote=False):
        return [
            val['id'][:-3] if justQuote else val['id'] for val in
            self._pullData('/public/symbol')
            if 'BTC' == val['id'][-3:]
        ]

    def getAssetPrice(self, sym, dir='buy'):
        tickData = self._pullData('/public/orderbook/%s' % sym, params={'limit': 1})
        return tickData['bid' if dir == 'sell' else 'ask'][0]['price']
