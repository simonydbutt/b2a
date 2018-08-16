from Pipeline_.main.PullData._Pull import _Pull


class PullHadax(_Pull):

    """
        Initially using for CommitValue
        # TODO: add amount to getAssetPrice to get the exact price will buy at
    """

    def __init__(self):
        _Pull.__init__(self)
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

