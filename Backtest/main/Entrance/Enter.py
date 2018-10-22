from Backtest.main.Data.Load import Load
from Backtest.main.Utils.TimeUtil import TimeUtil
from Backtest.main.Visual.CandlestickChart import CandlestickChart
from Backtest.main.Entrance.lib import *


class Enter:

    """
        Breaking change, fixed isFeasible and pivots, rest down...
    """

    def __init__(
        self,
        db,
        assetList,
        granularity,
        stratDict,
        startTime=1483228800,
        endTime=1527811200,
    ):
        self.L = Load(db)
        self.assetList = assetList
        self.stratDict = stratDict
        self.dfDict = {
            asset: self.L.loadOne(
                col="%s_%s" % (asset, granularity), timeStart=startTime, timeEnd=endTime
            )
            for asset in assetList
        }

    def run(self):
        enterAtDict = {asset: {"buy": [], "sell": []} for asset in self.assetList}
        for asset in self.dfDict.keys():
            positionDict = eval(self.stratDict["stratName"])(
                df=self.dfDict[asset], params=self.stratDict
            ).run()
            enterAtDict[asset]["buy"] = list(positionDict["buy"])
            enterAtDict[asset]["sell"] = list(positionDict["sell"])
        return enterAtDict


# T = TimeUtil()
# E = Enter(db='bitmex', assetList=['XBTUSD'], granularity='5m',
#           stratDict={'stratName': 'Pivots'})
# enterDict = E.run()
# print(enterDict)
# for enterAt in enterDict['ETHBTC']:
#     CandlestickChart().plotStrat(E.dfDict['ETHBTC'], timeStart=enterAt - T.bin2TS['2h']*5,
#                                  timeEnd=enterAt + T.bin2TS['2h']*15, vol=True)
