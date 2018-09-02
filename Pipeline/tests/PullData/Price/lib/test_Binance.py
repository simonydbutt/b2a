from Pipeline.main.PullData.Price.lib.Binance import Binance
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from Pipeline.main.Utils.AddLogger import AddLogger
import time

"""
    Tests binance connection and makes sure time is in sync
    * Assumes time sync within 10 seconds is okay 
"""

dbPath = 'Pipeline/DB/test'
CCD = CreateCleanDir(filePathList=['%s/CodeLogs' % dbPath])


def test_connection():
    CCD.create()
    AL = AddLogger(dirPath='%s/CodeLogs' % dbPath, stratName='test_Binance')
    PB = Binance(logger=AL.logger)
    assert PB._pullData('/api/v1/ping') == {}
    CCD.clean()


def test_getCandles():
    CCD.create()
    AL = AddLogger(dirPath='%s/CodeLogs' % dbPath, stratName='test_Binance')
    PB = Binance(logger=AL.logger)
    data = PB.getCandles('ETHBTC', 5, 86400, columns=['TS', 'open', 'high', 'low', 'close', 'takerQuoteVol'], lastReal=True)
    assert len(data) == 5
    assert list(data) == ['TS', 'open', 'high', 'low', 'close', 'takerQuoteVol']
    CCD.clean()


if __name__ == '__main__':
    test_connection()
    test_getCandles()
