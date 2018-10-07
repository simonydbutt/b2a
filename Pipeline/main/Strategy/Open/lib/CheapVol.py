from Pipeline.main.PullData.Price.Pull import Pull
from pymongo import MongoClient
from datetime import datetime
import numpy as np
import pandas as pd
import Settings
import logging
import yaml
import time


class CheapVol:

    """
        Profits from buying shitcoins in accumulation phase.
        Enters when price is still cheap and volume spikes

        Config Requirements:
            - periodsMA
            - periodsVolLong
            - periodsVolShort
            - volCoef
            - bolStd
    """

    def __init__(self, stratName, assetList, isTest=False):
        logging.debug('Initialising CheapVol()')
        pd.options.mode.chained_assignment = None
        self.assetList = assetList
        self.isTest = isTest
        with open('%s/Pipeline/resources/%s/config.yml' % (Settings.BASE_PATH, stratName)) as configFile:
            params = yaml.load(configFile)
            self.enterParams = params['enter']
            self.exchangeList = params['assetSelection']['exchangeList']
        self.db = MongoClient('localhost', 27017)[stratName]
        self.col = self.db['PastPriceAction']
        self.init()

    def _initSingle(self, asset, exchange):
        logging.debug('Starting CheapVol._initSingle(asset=%s)' % asset)
        try:
            pullData = Pull().candles(
                asset='%sBTC' % asset,
                exchange=exchange,
                limit=max(self.enterParams['periodsMA'], self.enterParams['periodsVolLong']) + 1,
                interval=self.enterParams['granularity'])
            priceList = list(pullData['close'])[-self.enterParams['periodsMA']:]
            volList = list(pullData['volume'])[-self.enterParams['periodsVolLong']:]
            if len(priceList) == self.enterParams['periodsMA'] and len(volList) == self.enterParams['periodsVolLong']:
                self.col.insert_one({
                    'asset': asset,
                    'price': priceList,
                    'vol': volList
                })
            else:
                logging.info('Not enough data for asset: %s' % asset)
        except IndexError:
            logging.warning('Failure on asset: %s' % asset)
        time.sleep(1.5)

    def init(self):
        """
            Creates mongo collection which contains the price action data required for CheapVol
        """
        logging.debug('Starting CheapVol.init()')
        if 'PastPriceAction' in self.db.collection_names():
            self.db.drop_collection('PastPriceAction')
        for asset, exchange in self.assetList:
            self._initSingle(asset, exchange)
        logging.info('Initialised PastPriceAction collection')

    def _getPADict(self, exchange):
        logging.debug('Starting CheapVol._getPADict()')
        startTS = int(time.time() - self.enterParams['granularity'])
        dateStart = datetime.fromtimestamp(startTS).strftime('%Y-%m-%dT%H:%M:%S.000Z')
        return Pull().getPriceAction(exchange=exchange, startDate=dateStart, baseAsset='BTC')

    def before(self):
        """
            Runs before CheapVol on each asset and updates the mongo collection
        """
        logging.debug('Starting CheapVol.before()')
        newPA = {}
        for exchange in self.exchangeList:
            newPA.update(self._getPADict(exchange=exchange))
        for assetDict in list(self.col.find()):
            assetDict['price'] = assetDict['price'][1:] + [newPA[assetDict['asset']]['price']]
            assetDict['vol'] = assetDict['vol'][1:] + [newPA[assetDict['asset']]['vol']]
            assetDict.pop('_id', None)
            self.col.find_one_and_replace({'asset': assetDict['asset']}, assetDict)

    def run(self, asset):
        logging.debug('Starting CheapVol.run(asset=%s)' % asset)
        assetData = self.col.find_one({'asset': asset})
        if assetData:
            volL = np.round(np.nanmean(np.array(assetData['vol']).astype(np.float)), 5)
            volS = np.round(np.nanmean(np.array(assetData['vol'][-self.enterParams['periodsVolShort']]).astype(np.float)), 5)
            priceData = np.array(assetData['price']).astype(np.float)
            bolDown = np.nanmean(priceData) - self.enterParams['bolStd'] * np.nanstd(priceData)
            logging.debug('volL: %s, volS: %s, price: %s, bolDown: %s' % (volL, volS, priceData[-1], bolDown))
            return volS > self.enterParams['volCoef'] * volL and priceData[-1] < bolDown
        else:
            return False
