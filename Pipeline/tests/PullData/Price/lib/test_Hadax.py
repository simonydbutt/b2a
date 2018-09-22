from Pipeline.main.PullData.Price.lib.Hadax import Hadax
import logging


def test_getCandles():
    PH = Hadax()
    data = PH.getCandles(asset='ETHBTC', limit=5, interval=3600, columns=['TS', 'open', 'close', 'low', 'high'],
                         lastReal=True)
    assert len(data) == 5
    assert list(data) == ['TS', 'open', 'close', 'low', 'high']


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_getCandles()