from Pipeline.main.Utils.ExchangeUtil import ExchangeUtil


def test_exchangeUtil():
    assert ExchangeUtil('Binance').candlestickInterval(60) == '1m'
    assert ExchangeUtil('Hadax').candlestickColumns() == ['TS', 'open', 'close', 'low', 'high', 'amount', 'vol', 'count']
    assert ExchangeUtil('Binance').fees() == 0.001


if __name__ == '__main__':
    test_exchangeUtil()