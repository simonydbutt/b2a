from Pipeline.main.AssetSelection.Select import Select
from Pipeline.main.AssetSelection.lib.All import All
from Pipeline.tests.CreateCleanDir import CreateCleanDir
import Settings
import logging
import yaml


CCD = CreateCleanDir(['Pipeline/resources/testSelect'])


def test_assets():
    CCD.create()
    config = {'assetSelection': {'name': 'All', 'baseAsset': 'BTC', 'exchangeList': ['Binance']}}
    with open('%s/Pipeline/resources/testSelect/config.yml' % Settings.BASE_PATH, 'w') as configFile:
        yaml.dump(config, configFile)
    assert Select('testSelect').assets() == All(config).getAssets()
    CCD.clean()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_assets()