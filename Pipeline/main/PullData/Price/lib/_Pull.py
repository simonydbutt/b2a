from Pipeline.main.Utils.EmailUtil import EmailUtil
import requests
import json
import time
import pandas as pd


class _Pull:

    """
        **TODO: on getAssetPrcie: add amount to getAssetPrice to get the exact price will buy at
    """


    def __init__(self, logger):
        self.logger = logger
        self.baseURL = ''

    def _pullData(self, endPoint, params=None, isTest=False, testReq='', testReq2=''):
        req = requests.get(self.baseURL + endPoint, params=params) if not isTest else testReq
        if req.status_code == 200:
            return json.loads(req.content.decode('utf-8')) if not isTest else 1
        elif req.status_code == 429:
            self.logger.warning('Rate limit hit, 30 second sleep')
            time.sleep(30 if not isTest else 0.001)
            req = requests.get(self.baseURL + endPoint, params=params) if not isTest else testReq2
            if req.status_code == 429:
                errorMsg = 'Rate limit error after timeout'
                self.logger.error(errorMsg)
                if not isTest:
                    EmailUtil().errorExit(file='_Pull', funct='_pullData', message=errorMsg)
                else:
                    return 2
            else:
                self.logger.info('Rate limit back to normal')
                return json.loads(req.content.decode('utf-8')) if not isTest else 3
        else:
            errorMsg = 'pullData requests error with error code %s' % req.status_code
            self.logger.error(errorMsg)
            if not isTest:
                EmailUtil().errorExit(file='_Pull', funct='_pullData', message=errorMsg)
            else:
                return 4

    def getBTCAssets(self, justQuote=False):
        return []

    def getCandles(self, asset, limit, interval, columns, lastReal):

        return pd.DataFrame([], columns=columns)

    def getAssetPrice(self, sym, dir):
        # TODO: change to add the exact amount required
        return -1