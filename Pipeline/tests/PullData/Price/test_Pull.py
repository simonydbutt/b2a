from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.main.PullData.Price.lib.Binance import Binance
from Pipeline.main.Utils.AddLogger import AddLogger
from Pipeline.tests.CreateCleanDir import CreateCleanDir

"""
    TODO: Add to this when adding other exchanges
"""


CCD = CreateCleanDir(filePathList=['Pipeline/tests/test_DB/CodeLogs/test_Pull'])


def test_BTCAssets():
    CCD.create()
    AL = AddLogger('Pipeline/tests/test_DB/CodeLogs/test_Pull', stratName='test_Pull')
    PB = Binance(logger=AL.logger)
    P = Pull(exchange='Binance', logger=AL.logger)
    assert PB.getBTCAssets() == P.BTCAssets()
    CCD.clean()


if __name__ == '__main__':
    test_BTCAssets()