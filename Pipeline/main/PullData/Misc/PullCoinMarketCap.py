from bs4 import BeautifulSoup
import requests


class PullCoinMarketCap:

    def __init__(self):
        self.baseUrl = 'https://coinmarketcap.com'

    def getMarketCapDict(self):
        sp = BeautifulSoup(requests.get('%s/all/views/all' % self.baseUrl).content, 'html.parser')
        mcDict = {}
        for val in sp.find('tbody').find_all('tr'):
            sym = val.find('a', class_='link-secondary').get_text()
            if sym not in mcDict.keys():
                mcDict[sym] = float(
                    val.find('td', class_='market-cap').get_text().replace('\n', '')
                        .replace('$', '').replace(',','').replace('?', '0'))
        return mcDict
