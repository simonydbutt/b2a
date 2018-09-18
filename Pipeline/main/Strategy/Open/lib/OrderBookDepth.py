from Pipeline.main.PullData.Price.Pull import Pull
import numpy as np
import Settings
import logging
import yaml
import time


class OrderBookDepth:

    """
        Buys when there is a big order book discrepancy

        Config Requirements:
            - period
            - bookDepth (default: 50)
            - numTrades (default: 1000)
            - diffVals (default: [5, 10, 20]
            - enterPercent
    """

    def __init__(self, stratName, isTest):
        logging.debug('Initialising OrderBookDepth()')
        self.isTest = isTest
        with open('%s/Pipeline/resources/%s/config.yml' % (Settings.BASE_PATH, stratName)) as configFile:
            self.enterParams = yaml.load(configFile)['enter']

    def getTradesDiff(self, asset, exchange):
        logging.debug('Starting OrderBookDepth.getTradesDiff')
        vals = Pull().getTrades(asset=asset, exchange=exchange, limit=self.enterParams['numTrades'], maxTime=self.enterParams['period'])
        if len(vals) != 0:
            vL = len(vals)
            meanVal = round(float(np.mean(vals['Qty'])))
            diff = round(sum(vals[vals['Buy/Sell'] == 'b']['Qty']) - sum(vals[vals['Buy/Sell'] == 's']['Qty']))
            return [diff - (vL / diffVal) * meanVal for diffVal in self.enterParams['diffVals']] + [diff] + \
                   [diff + (vL / diffVal) * meanVal for diffVal in self.enterParams['diffVals']]
        else:
            return -1

    def walkDown(self, orderBook, qty):
        logging.debug('Starting OrderBookDepth.walkDown')
        buySell = 'bids' if qty > 0 else 'asks'
        orderList = [val[0] for val in orderBook[buySell]]
        qty = abs(qty)
        n = 0
        while qty > 0 and n < len(orderBook['bids']):
            qty -= orderList[n]
            n += 1
        return orderBook[buySell][n - 1][1]

    def run(self, asset, exchange, testData=None):
        logging.debug('Starting OrderBookDepth.run')
        tradeDiff = self.getTradesDiff(asset=asset, exchange=exchange)
        priceList = []
        if tradeDiff != -1:
            orderBook = Pull().getOrderBook(exchange=exchange, asset=asset, limit=self.enterParams['bookDepth'])
            for tradeQty in tradeDiff:
                priceList.append(self.walkDown(orderBook, tradeQty))
            price_ = round(float(np.mean(priceList)), 8)
            pDiff = round(price_/orderBook['bids'][0][1], 8)
            if pDiff > 1:
                logging.debug('Asset: %s, pDiff: %s' % (asset, pDiff))
            if pDiff > self.enterParams['enterPercent']:
                return True
            else:
                return False
        else:
            logging.debug('Data is incomplete')
            return False
