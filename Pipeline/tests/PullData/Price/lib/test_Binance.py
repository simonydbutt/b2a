from Pipeline.main.PullData.Price.lib.Binance import Binance
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from Pipeline.main.Utils.AddLogger import AddLogger
import time

"""
    Tests binance connection and makes sure time is in sync
    * Assumes time sync within 10 seconds is okay 
"""

CCD = CreateCleanDir(filePathList=['Pipeline/tests/test_DB/CodeLogs/test_Binance'])


def test_connection():
    CCD.create()
    AL = AddLogger('Pipeline/tests/test_DB/CodeLogs/test_Binance', stratName='test_Pull')
    PB = Binance(logger=AL.logger)
    assert PB._pullData('/api/v1/ping') == {}
    assert round(PB._pullData('/api/v1/time')['serverTime']/10000) == round(time.time()/10)
    CCD.clean()


def test_getCandles():
    CCD.create()
    AL = AddLogger('Pipeline/tests/test_DB/CodeLogs/test_Binance', stratName='test_Pull')
    PB = Binance(logger=AL.logger)
    data = PB.getCandles('ETHBTC', 5, 86400, columns=['TS', 'open', 'high', 'low', 'close', 'takerQuoteVol'], lastReal=True)
    assert len(data) == 5
    assert list(data) == ['TS', 'open', 'high', 'low', 'close', 'takerQuoteVol']
    CCD.clean()


if __name__ == '__main__':
    test_connection()
    test_getCandles()