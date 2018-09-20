from Pipeline.main.PullData.Price.Pull import Pull
from Pipeline.main.PullData.Price.lib.Binance import Binance
from Pipeline.main.PullData.Price.lib.Hadax import Hadax
import logging


# *TODO hadax seems to be playing w. their api atm, will turn on when they stop...
# def test_BTCAssets():
#     PH = Hadax()
#     P = Pull()
#     print(PH.getBTCAssets())
#     print(P.BTCAssets(exchange='Hadax'))
#     assert PH.getBTCAssets() == P.BTCAssets(exchange='Hadax')


def test_candles():
    BinanceData = Binance().getCandles(
        asset='LTCBTC', limit=5, interval=300, columns=['TS', 'open'], lastReal=True)
    PullData = Pull().candles(
        exchange='Binance', asset='LTCBTC', limit=5, interval=300, columns=['TS', 'open'], lastReal=True)
    assert PullData.equals(BinanceData) and len(PullData) != 0


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    #test_BTCAssets()
    test_candles()