from Pipeline.main.PullData.PullHitBTC import PullHitBTC
from Pipeline.main.PullData.PullBinance import PullBinance
from Pipeline.main.PullData.PullHadax import PullHadax
from Pipeline.main.PullData.PullRepo import PullRepo
from Pipeline.main.PullData.PullCoinMarketCap import PullCoinMarketCap
import numpy as np
import pandas as pd


class GetAssets:

    def __init__(self, logger, minCommits=300, numAssets=10):
        self.numAssets = numAssets
        self.commitList = PullRepo(minCommits=minCommits).get3MonthCommits()
        logger.info('Pulled coin commit data')
        self.getMarketCaps = PullCoinMarketCap().getMarketCapDict()
        logger.info('Pulled coin market cap data')
        self.pullExchangeDict = {
            'Binance': PullBinance(),
            'HitBTC': PullHitBTC(),
            'Hadax': PullHadax()
        }
        self.exchangeDict = self.getExchangeCoins()

    def getExchangeCoins(self):
        exchangeDict = {}
        for ex in self.pullExchangeDict.keys():
            exBTCAssets = self.pullExchangeDict[ex].getBTCAssets(justQuote=True)
            for asset in exBTCAssets:
                if asset not in exchangeDict.keys():
                    exchangeDict[asset] = ex
        return exchangeDict

    def getDF(self):
        na = 0
        compList = []
        for val in self.commitList:
            mc = self.getMarketCaps[val[1]] if val[1] in self.getMarketCaps.keys() else 0
            ex = self.exchangeDict[val[1]] if val[1] in self.exchangeDict.keys() else '-'
            if mc != 0 and ex != '-':
                compList.append(val + [mc, val[2]/np.sqrt(mc), ex])
            else:
                na += 1
        print('%s Assets not enough data' % na)
        return pd.DataFrame(compList, columns=['Name', 'Symbol', 'Commits', 'MarketCap', 'Commit/MC', 'Exchange'])\
            .sort_values(by='Commit/MC', ascending=False).reset_index(drop=True)

    def allocatePositions(self):
        df = self.getDF()[:self.numAssets]
        df['Allocate'] = round(np.sqrt(df['Commit/MC'])/sum(np.sqrt(df['Commit/MC'])), 2)
        positionDict = {}
        for i in range(len(df)):
            pos = df.iloc[i]
            positionDict[pos['Symbol']] = {'Name': pos['Name'], 'Symbol': pos['Symbol'],
                                           'Exchange': pos['Exchange'], 'Allocate': pos['Allocate']}
        return positionDict

