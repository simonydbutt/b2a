from Pipeline.main.PullData.Price.Pull import Pull
import numpy as np


class All:

    def __init__(self, config, logger):
        self.exchangeList = config['assetSelection']['exchangeList']
        self.baseAsset = config['assetSelection']['baseAsset']
        self.logger = logger

    def getAssets(self):
        assetList = []
        for exchange in self.exchangeList:
            if self.baseAsset == 'BTC':
                tmpList = Pull(exchange=exchange, logger=self.logger).BTCAssets()
                addedAssets = [val.lower() for val in np.array(assetList)[:,0]] if len(assetList) != 0 else []
                assetList += [(asset, exchange) for asset in tmpList if asset.lower() not in addedAssets]
        return assetList