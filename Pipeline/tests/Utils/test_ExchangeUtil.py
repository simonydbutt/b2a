from Pipeline.main.Utils.ExchangeUtil import ExchangeUtil


def test_exchangeUtil():
    assert ExchangeUtil('Binance').candlestickInterval(60) == '1m'
    assert ExchangeUtil('Hadax').candlestickColumns() == ['TS', 'open', 'close', 'low', 'high', 'amount', 'vol', 'count']


if __name__ == '__main__':
    test_exchangeUtil()