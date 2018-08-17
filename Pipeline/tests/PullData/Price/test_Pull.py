from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.main.PullData.Price.lib.Binance import Binance
from Pipeline.main.PullData.Price.lib.Hadax import Hadax
from Pipeline.main.Utils.AddLogger import AddLogger
from Pipeline.tests.CreateCleanDir import CreateCleanDir

"""
    TODO: Add to this when adding other exchanges
"""


CCD = CreateCleanDir(filePathList=['Pipeline/tests/test_DB/CodeLogs/test_Pull'])


def test_BTCAssets():
    CCD.create()
    AL = AddLogger('Pipeline/tests/test_DB/CodeLogs/test_Pull', stratName='test_Pull')
    PH = Hadax(logger=AL.logger)
    P = Pull(exchange='Hadax', logger=AL.logger)
    assert PH.getBTCAssets() == P.BTCAssets()
    CCD.clean()


def test_candles():
    CCD.create()
    AL = AddLogger('Pipeline/tests/test_DB/CodeLogs/test_Pull', stratName='test_Pull')
    BinanceData = Binance(logger=AL.logger).getCandles(
        asset='LTCBTC', limit=5, interval=300, columns=['TS', 'open'], lastReal=True)
    PullData = Pull(exchange='Binance', logger=AL.logger).candles(
        asset='LTCBTC', limit=5, interval=300, columns=['TS', 'open'], lastReal=True)
    assert PullData.equals(BinanceData) and len(PullData) != 0
    CCD.clean()


if __name__ == '__main__':
    test_BTCAssets()
    test_candles()