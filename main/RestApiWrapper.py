import requests
import json
import numpy as np
import pandas as pd


class RestApiWrapper:

    def __init__(self, assets=('XBTUSD','XBTM18', 'XBTU18')):
        self._baseUrl = 'https://www.bitmex.com/api/v1'
        self.assets = assets

    def _getData(self, url, params=None):
        data = requests.get(url, params=params).content.decode("utf-8")
        return json.loads(data)

    def pullQuotes(self, symbol):
        params = {'symbol': symbol, 'depth':1}
        return self._getData(self._baseUrl + '/orderBook/L2', params=params)

    def getLatest(self, symbol):
        q = self.pullQuotes(symbol=symbol)
        qSell = q[0]; qBuy = q[1]
        if qSell['price'] - qBuy['price'] < 5:
            return (qSell['price'] + qBuy['price'])/2
        else:
            print('Not enough liquidity')
            return -1

    def allXBTQuotes(self):
        latestData = []
        for asset in self.assets:
            latestData.append(self.getLatest(symbol=asset))
        latestData.append(np.abs(latestData[0] - latestData[1]) if latestData[0] != -1 or latestData[1] != -1 else -1)
        latestData.append(np.abs(latestData[0] - latestData[2]) if latestData[0] != -1 or latestData[2] != -1 else -1)
        latestData.append(np.abs(latestData[1] - latestData[2]) if latestData[1] != -1 or latestData[2] != -1 else -1)
        return pd.DataFrame([latestData], columns=['P', 'M', 'U', 'spreadPM', 'spreadPU', 'spreadUM'])
