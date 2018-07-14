from Backtest.main.Attributes.lib import *
from Backtest.main.Data.Load import Load
from Backtest.main.Entrance.lib import *


class Enter:

    """

    """

    def __init__(self, db, assetList, granularity, stratDict, startTime=1483228800, endTime=1527811200):
        self.L = Load(db)
        self.assetList = assetList
        self.stratDict = stratDict
        self.dfDict = {asset: self.L.loadOne(col='%s_%s' % (asset, granularity), timeStart=startTime, timeEnd=endTime)
                       for asset in assetList}

    def run(self):
        enterAtDict = {asset: [] for asset in self.assetList}
        for asset in self.dfDict.keys():
            enterTmp = []
            for strat in self.stratDict.keys():
                enterTmp.append(eval(strat)(df=self.dfDict[asset], params=self.stratDict[strat]).run())
            enterAtList = enterTmp[0]
            if len(enterTmp) > 1:
                for i in enterTmp[1:]:
                    enterAtList.intersection_update(i)
            enterAtDict[asset] = enterAtList
        return enterAtDict


#print(Enter('binance', ['XMRBTC', 'LTCBTC', 'BNBBTC', 'ETHBTC', 'NULSBTC'], '12h', {'IsFeasible': {}}).run())
