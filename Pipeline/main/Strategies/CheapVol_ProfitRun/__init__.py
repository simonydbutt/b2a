import json
import Settings
from Pipeline.main.PullData.PullBinance import PullBinance
from Pipeline.main.Strategies.CheapVol_ProfitRun.IsCheapVol import IsCheapVol
from tinydb import TinyDB, Query

# TODO

configDB = TinyDB('%s/Pipeline/DB/configs/CheapVol_ProfitRun.json' % Settings.BASE_PATH)
positionsDB = TinyDB('%s/Pipeline/DB/Positions.json' % Settings.BASE_PATH)
P = PullBinance()

def getConfig(valName, table=None):
    q = Query()
    if table:
        return configDB.table(table).all()[0][valName]
    else:
        return configDB[valName]


for asset in P.getBTCAssets():
    q = Query()
    if len(positionsDB.table('Current').search(q.Asset == asset)) == 0:
        IsCheapVol(P.getCandles(asset, ))
