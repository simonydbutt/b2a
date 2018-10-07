from Pipeline.main.PullData.Price.Pull import Pull
import numpy as np
import logging


class AllNomics:

    """
        *TODO: AllNomics --> All
        deprecate All
    """

    def __init__(self, config):
        logging.debug('Initialising AllNomics()')
        self.exchangeList = config['assetSelection']['exchangeList']
        self.baseAsset = config['assetSelection']['baseAsset']

    def getAssets(self):
        logging.debug('Starting AllNomics.getAssets')
        logging.debug('Exchanges analysed: %s' % self.exchangeList)
        logging.debug('Base Asset: %s' % self.baseAsset)
        assetList = []
        for exchange in self.exchangeList:
            logging.debug('Starting exchange: %s' % exchange)
            if self.baseAsset == 'BTC':
                tmpListNomics = Pull().BTCAssets(exchange='Nomics', exchange_=exchange)
                tmpListEx = Pull().BTCAssets(exchange=exchange, justQuote=True)
                tmpList = list(set(tmpListNomics) & set(tmpListEx))
                addedAssets = [val.lower() for val in np.array(assetList)[:, 0]] if len(assetList) != 0 else []
                assetList += [(asset, exchange) for asset in tmpList if asset.lower() not in addedAssets]
        logging.debug('Ending All.getAssets')
        logging.debug('Assetlist length: %s' % len(assetList))
        return assetList
