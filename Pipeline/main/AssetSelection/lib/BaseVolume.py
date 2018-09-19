from Pipeline.main.PullData.Price.Pull import Pull
from pymongo import MongoClient
import logging


class BaseVolume:

    """
        Requires in config:
            - minVol (default: 0.05)
            - maxVol (default: 0.1)
            - minTrades (default: 2000)
    """

    def __init__(self, config):
        logging.debug('Initialising BaseVolume()')
        self.params = config['assetSelection']
        self.assetCol = MongoClient('localhost', 27017)[config['stratName']]['viableAssets']

    def createAssetList(self):
        tickerData = {
            val['symbol']: {
                'vol': float(val['quoteVolume']),
                'tradeCount': val['count'],
                'baseVol': float(val['volume'])
            } for val in Pull().getTickerStats(exchange='Binance') if 'BTC' in val['symbol']
        }
        coinList = []
        base = tickerData['BTCUSDT']['baseVol']
        for coin in [c for c in list(tickerData) if c != 'BTCUSDT']:
            if tickerData[coin]['tradeCount'] > self.params['minTrades'] and \
                    self.params['minVol']*base < tickerData[coin]['vol'] < self.params['maxVol'] * base:
                    coinList.append({
                        'asset': coin,
                        'exchange': 'Binance'
                    })
        self.assetCol.insert_many(coinList)

    def getAssets(self):
        logging.debug('Starting BaseVolume.getAssets')
        return [(val['asset'], val['exchange']) for val in list(self.assetCol.find())]



