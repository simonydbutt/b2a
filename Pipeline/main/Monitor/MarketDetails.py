from Pipeline.main.PullData.Misc.PullCoinMarketCap import PullCoinMarketCap
import numpy as np


class MarketDetails:

    """
        Period:
            short: 1h, mid: 24h, long: 1w
    """

    def __init__(self):
        self.pull = PullCoinMarketCap()

    def getBTCPrice(self):
        # *TODO
        pass

    def multiTicks(self, tickSizeList):
        coinPage = self.pull.getPage()
        tickDict = {}
        for tickSize in tickSizeList:
            tickDict[str(tickSize)] = self.getTick(noCoins=tickSize, page=coinPage)
        return tickDict

    def getTick(self, noCoins=1000, page=None):
        n = 0
        tickList = []
        coinPage = self.pull.getPage() if not page else page
        for coinDiv in coinPage.find('tbody').find_all('tr')[:noCoins]:
            try:
                percentSect = coinDiv.find_all('td', class_='percent-change')
                if len(percentSect) == 3:
                    tickList.append([1 if float(val['data-sort']) > 0 else -1 for val in percentSect])
                else:
                    n += 1
            except ValueError:
                n += 1
        ticks = [sum(tL) for tL in np.transpose(tickList)]
        #print(tickList)
        return {'short': ticks[0], 'mid': ticks[1], 'long': ticks[2]}
