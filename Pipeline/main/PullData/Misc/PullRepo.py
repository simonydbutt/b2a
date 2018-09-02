from bs4 import BeautifulSoup
import requests


class PullRepo:

    """
        ***TODO: Eventually build out to pull actual repos, not webscrape
    """

    def __init__(self, minCommits):
        self.baseUrl = 'https://cryptomiso.com'
        self.minCommits = minCommits

    def get3MonthCommits(self):
            repoUrl = '%s/months_3.html' % self.baseUrl
            sp = BeautifulSoup(requests.get(repoUrl).content, 'html.parser')
            coinList = [
                [val[0], val[1], int(val[2])] for val in
                [(
                    div.get_text().split(' ')[1].lower(),
                    div.find('a').get_text(),
                    div.find('span', class_='badge').get_text()[:-8].replace(',', '')
                )
                    for div in sp.find_all('h4', class_='card-title')]
                if val[2] != ''
            ]
            return [val for val in coinList if val[2] > self.minCommits]
