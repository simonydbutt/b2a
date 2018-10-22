from Backtest.main.Exit.lib import *
from Backtest.main.Entrance.Enter import Enter


class Exit:

    """
        ExitStrat = (stratName, params)
    """

    def __init__(self, Entrance, exitStrat):
        self.E = Entrance
        self.exitStrat = exitStrat
        self.dfDict = self.E.dfDict
        self.assetList = self.E.assetList
        self.enterList = self.E.run()

    def run(self):
        positionDict = {asset: [] for asset in self.assetList}
        for asset in self.assetList:
            positionDict[asset] = eval(self.exitStrat[0])(
                df=self.dfDict[asset],
                params=self.exitStrat[1],
                enterList=self.enterList[asset],
            ).run()
        return positionDict


# E = Enter(db='binance', assetList=['XMRBTC', 'LTCBTC', 'ETHBTC', 'XRPBTC', 'NULSBTC'], granularity='12h',
#           stratDict={'Rand': {'sampSize': 10}})
# print(Exit(E, ('StdExit', {})).run())
