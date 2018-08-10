from Pipeline.main.Finance.PaperGains import PaperGains
import Settings
import yaml
from tinydb import TinyDB


class OpenClosePosition:

    def __init__(self, stratName, fees=0.001, dbPath='Pipeline/DB'):
        self.fees = fees
        with open('%s/%s/Capital.yml' % (Settings.BASE_PATH, dbPath)) as capitalFile:
            self.capitalDict = yaml.load(capitalFile)
        with open('%s/%s/Configs/%s.yml' % (Settings.BASE_PATH, dbPath, stratName)) as configFile:
            self.configFile = yaml.load(configFile)
        self.transLogDB = TinyDB('%s/Pipeline/%s/TransactionLog.ujson' % (Settings.BASE_PATH, dbPath))

    def openPosition(self, openDict):
        self.capitalDict['liquidCurrent'] -= openDict['capAllocated']
        self.capitalDict['percentAllocated'] = 100*round(1 - self.capitalDict['liquidCurrent']/self.capitalDict['paperCurrent'], 2)

    def closePosition(self, tradeDict):
        P = PaperGains(fees=self.fees)
        tradeDict['realPnL'] = tradeDict['capitalAllocated']*((1 - self.fees)*tradeDict['closePrice'] -
                                                              (1 + self.fees)*tradeDict['openPrice'])
        tradeDict['percentPnL'] = tradeDict['closePrice'] / tradeDict['openPrice'] - 1
        self.transLogDB.insert(tradeDict)
        self.capitalDict['liquidCurrent'] += (tradeDict['amountHeld'] / tradeDict['closePrice'])*(1-self.fees)
        self.capitalDict['paperCurrent'] = float(self.capitalDict['liquidCurrent'] + P.calc())
        self.capitalDict['paperPnL'] = float(self.capitalDict['paperCurrent'] / self.capitalDict['initialCapital'])
        self.capitalDict['percentAllocated'] = float(P.allocated(liquidCurrent=self.capitalDict['liquidCurrent']))
        pStats = self.configFile['performance']
        self.configFile['performance']['percentPnL'] = (pStats['percentPnL']*pStats['numTrades'] +
                                                        tradeDict['percentPnL']) / (pStats['percentPnL'] + 1)
        self.configFile['performance']['maxGain'] = max(pStats['maxGain'], tradeDict['percentPnL'])
        self.configFile['performance']['maxLoss'] = min(pStats['maxLoss'], tradeDict['percentPnL'])
        self.configFile['performance']['numTrades'] += 1
        isWin = 1 if tradeDict['percentPnL'] > 0 else 0
        self.configFile['performance']['winLoss'] = (pStats['winLoss'] * pStats['numTrades'] + isWin) / \
                                                    (pStats['numTrades'] + 1)
        self.configFile['performance']['avgPeriods'] = (pStats['avgPeriods'] * pStats['numTrades'] +
                                                        tradeDict['periods']) / (pStats['numTrades'] + 1)

    def add2Books(self):
        with open('%s/Pipeline/DB/Capital.yml' % Settings.BASE_PATH, 'w') as capFile:
            yaml.dump(self.capitalDict, capFile)