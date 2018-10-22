class TestingStrat:
    def __init__(self, stratName, assetList, isTest=False):
        pass

    def before(self):
        pass

    def run(self, asset):
        return asset != "LTC"
