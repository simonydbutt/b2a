from Pipeline.main.AssetSelection.lib.All import All
from Pipeline.main.PullData.Price.Pull import Pull
import logging


def test_getAssets():
    config = {'assetSelection': { 'baseAsset': 'BTC', 'exchangeList': ['Hadax', 'Binance'], 'name': 'All'}}
    PH = Pull().BTCAssets('Hadax')
    pullVals = [(val, 'Hadax') for val in PH] + [(val, 'Binance') for val in Pull().BTCAssets('Binance')
                                                 if val not in PH]
    allVals = All(config).getAssets()
    assert allVals == pullVals


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_getAssets()