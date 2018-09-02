from Pipeline.main.PullData.Price.Pull import Pull


class All:

    def __init__(self, config, logger):
        self.exchangeList = config['exchangeList']
        self.baseAsset = config['baseAsset']
        self.logger = logger

    def getAssets(self):
        assetList = []
        for exchange in self.exchangeList:
            if self.baseAsset == 'BTC':
                tmpList = Pull(exchange=exchange, logger=self.logger).BTCAssets()
                assetList += [(asset, exchange) for asset in tmpList]
        return assetList