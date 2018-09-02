from Pipeline.main.AssetSelection.lib.All import All
from Pipeline.main.Utils.AddLogger import AddLogger
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from Pipeline.main.PullData.Price.Pull import Pull


dbPath = 'Pipeline/DB/test'
CCD = CreateCleanDir(filePathList=['%s/CodeLogs' % dbPath])


def test_getAssets():
    CCD.create()
    AL = AddLogger(dirPath='%s/CodeLogs' % dbPath, stratName='test_All').logger
    config = {
        'baseAsset': 'BTC',
        'exchangeList': ['Hadax', 'Binance'],
        'name': 'All'
    }
    PH = Pull('Hadax', AL).BTCAssets()
    pullVals = [(val, 'Hadax') for val in PH] + [(val, 'Binance') for val in Pull('Binance', AL).BTCAssets()
                                                 if val not in PH]
    allVals = All(config, AL).getAssets()
    assert allVals == pullVals
    CCD.clean()


if __name__ == '__main__':
    test_getAssets()