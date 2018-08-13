import json
import requests
import logging
import time


class _Pull():

    def __init__(self):
        self.baseUrl = ''

    def _pullData(self, endPoint, params=None):
        req = requests.get(self.baseUrl + endPoint, params=params)
        if req.status_code == 200:
            return json.loads(req.content.decode('utf-8'))
        elif req.status_code == 429:
            logging.warning('binance rate limit hit, 30 second sleep')
            time.sleep(30)
            req = requests.get(self.baseUrl + endPoint, params=params)
            if req.status_code == 429:
                logging.error('Rate limit error after timeout')
            else:
                logging.info('Rate limit back to normal')
                return json.loads(req.content.decode('utf-8'))
        else:
            logging.error('pullData requests error with error code %s' % req.status_code)
