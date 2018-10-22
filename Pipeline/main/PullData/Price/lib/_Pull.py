from Pipeline.main.Utils.EmailUtil import EmailUtil
import pandas as pd
import Settings
import hashlib
import logging
import requests
import hmac
import json
import time


class _Pull:

    """
        *TODO: bring more into this underlying Class
        **TODO: on getAssetPrcie: add amount to getAssetPrice to get the exact price will buy at
            - Have a limit to slidedown and lack of liquidity
        **TODO: when adding additional exchanges to same strat, normalise Volume field
    """

    def __init__(self, emailOnFailure=True):
        self.baseURL = ""
        self.emailOnFailure = emailOnFailure

    def _pullData(self, endPoint, params=None, isTest=False, testReq="", testReq2=""):
        logging.debug("Starting _Pull._pullData")
        logging.debug("Endpoint: %s, params: %s" % (endPoint, params))
        try:
            req = (
                requests.get(self.baseURL + endPoint, params=params)
                if not isTest
                else testReq
            )
        except OSError:
            EmailUtil().errorExit(
                file="_Pull", funct="_pullData", message="OS Error -> network down!"
            ) if self.emailOnFailure else None
            time.sleep(300)
            req = (
                requests.get(self.baseURL + endPoint, params=params)
                if not isTest
                else testReq
            )
        logging.debug("req status code: %s" % req.status_code)
        if req.status_code == 200:
            return json.loads(req.content.decode("utf-8")) if not isTest else 1
        elif req.status_code == 429:
            logging.warning("Rate limit hit, 30 second sleep")
            time.sleep(30 if not isTest else 0.001)
            req = (
                requests.get(self.baseURL + endPoint, params=params)
                if not isTest
                else testReq2
            )
            if req.status_code == 429:
                errorMsg = "Rate limit error after timeout"
                logging.error(errorMsg)
                if not isTest:
                    EmailUtil().errorExit(
                        file="_Pull", funct="_pullData", message=errorMsg
                    ) if self.emailOnFailure else None
                else:
                    return 2
            else:
                logging.info("Rate limit back to normal")
                return json.loads(req.content.decode("utf-8")) if not isTest else 3
        else:
            errorMsg = "pullData requests error with error code %s" % req.status_code
            logging.error(errorMsg)
            if not isTest:
                EmailUtil().errorExit(
                    file="_Pull", funct="_pullData", message=errorMsg
                ) if self.emailOnFailure else None
            else:
                return 4

    def _pullEncrypt(self, endPoint, paramString, isGet=True):
        logging.debug("Starting _Pull._pullEncrypt")
        sig = hmac.new(
            msg=paramString.encode("utf-8"),
            key=Settings.TRADE["sec"].encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()
        url = "%s/%s?%s" % (self.baseURL, endPoint, paramString)
        headers = {"X-MBX-APIKEY": Settings.TRADE["apiKey"]}
        params = {"signature": sig}
        req = (
            requests.get(url=url, headers=headers, params=params)
            if isGet
            else requests.post(url=url, headers=headers, params=params)
        )
        return json.loads(req.content.decode("utf-8"))

    def getBTCAssets(self, justQuote=False):
        logging.debug("Starting _Pull.getBTCAssets")
        return []

    def getCandles(self, asset, limit, interval, columns, lastReal):
        logging.debug("Starting _Pull.getCandles")
        return pd.DataFrame([], columns=columns)

    def getAssetPrice(self, sym, dir):
        logging.debug("Starting _Pull.getAssetPrice")
        return -1
