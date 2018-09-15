from Pipeline.main.AssetSelection.Select import Select
from Pipeline.main.AssetSelection.lib.All import All
import logging


def test_assets():
    config = {'assetSelection': {'name': 'All', 'baseAsset': 'BTC', 'exchangeList': ['Binance']}}
    assert Select(config).assets() == All(config).getAssets()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_assets()