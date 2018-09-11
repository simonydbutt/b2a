from Pipeline.main.PullData.Price.Pull import Pull
import numpy as np
import logging


class All:

    def __init__(self, config):
        self.exchangeList = config['assetSelection']['exchangeList']
        self.baseAsset = config['assetSelection']['baseAsset']

    def getAssets(self):
        logging.debug('Starting All.getAssets')
        logging.debug('Exchanges analysed: %s' % self.exchangeList)
        logging.debug('Base Asset: %s' % self.baseAsset)
        assetList = []
        for exchange in self.exchangeList:
            logging.debug('Starting exchange: %s' % exchange)
            if self.baseAsset == 'BTC':
                tmpList = Pull(exchange=exchange).BTCAssets()
                addedAssets = [val.lower() for val in np.array(assetList)[:,0]] if len(assetList) != 0 else []
                assetList += [(asset, exchange) for asset in tmpList if asset.lower() not in addedAssets]
        logging.debug('Ending All.getAssets')
        return assetList
