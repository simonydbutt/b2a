from Pipeline.main.PullData.Price.Pull import Pull
import logging


class AccountUtil:

    def __init__(self, exchange, isTest):
        logging.debug('Initialising AccountUtil()')
        self.exchange = exchange
        self.isTest = isTest
        self.P = Pull()

    def _calcValue(self, accountDetails):
        logging.debug('Starting AccountUtil._calcValue')
        value = 0
        for coin in [c for c in list(accountDetails) if c != 'BTC']:
            value += accountDetails[coin] * (self.P.assetPrice(exchange=self.exchange, asset='%sBTC' % coin, dir='sell') if \
                not self.isTest else self.isTest[coin])
        return value

    def getValue(self, initCapital, isTest=False):
        logging.debug('Starting AccountValue.getValue')
        capDict = {'initialCapital': initCapital}
        accountDetails = self.P.getAccount(exchange=self.exchange) if not isTest else isTest
        capDict['liquidCurrent'] = round(accountDetails['BTC'], 8)
        capDict['paperCurrent'] = round(capDict['liquidCurrent'] + self._calcValue(accountDetails), 8)
        capDict['paperPnL'] = round(capDict['paperCurrent'] / capDict['initialCapital'], 2)
        capDict['percentAllocated'] = round((capDict['paperCurrent'] - capDict['liquidCurrent'])/capDict['paperCurrent'], 2)
        return capDict
