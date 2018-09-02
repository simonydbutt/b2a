from Pipeline.main.PullData.Price.lib.Hadax import Hadax
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from Pipeline.main.Utils.AddLogger import AddLogger


dbPath = 'Pipeline/DB/test'
CCD = CreateCleanDir(filePathList=['%s/test_Hadax' % dbPath, '%s/test_Hadax/CodeLogs' % dbPath])


def test_getCandles():
    CCD.create()
    AL = AddLogger(db='test', stratName='test_Hadax')
    PH = Hadax(logger=AL.logger)
    data = PH.getCandles(asset='ETHBTC', limit=5, interval=3600, columns=['TS', 'open', 'close', 'low', 'high'],
                         lastReal=True)
    assert len(data) == 5
    assert list(data) == ['TS', 'open', 'close', 'low', 'high']
    CCD.clean()


if __name__ == '__main__':
    test_getCandles()