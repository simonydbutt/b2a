from Pipeline.main.AssetSelection.Select import Select
from Pipeline.main.AssetSelection.lib.All import All
from Pipeline.main.Utils.AddLogger import AddLogger
from Pipeline.tests.CreateCleanDir import CreateCleanDir


dbPath = 'Pipeline/DB/test'
CCD = CreateCleanDir(filePathList=['%s/test_Select' % dbPath, '%s/test_Select/CodeLogs' % dbPath])


def test_assets():
    CCD.create()
    config = {'assetSelection': {'name': 'All', 'baseAsset': 'BTC', 'exchangeList': ['Binance']}}
    AL = AddLogger(db='test', stratName='test_Select').logger
    assert Select(config, AL).assets() == All(config['assetSelection'], AL).getAssets()


if __name__ == '__main__':
    test_assets()