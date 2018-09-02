from Pipeline.main.Utils.ExchangeUtil import ExchangeUtil


def test_exchangeUtil():
    assert ExchangeUtil().candlestickInterval(60, exchange='Binance') == '1m'
    assert ExchangeUtil().candlestickColumns(exchange='Hadax') == ['TS', 'open', 'close', 'low', 'high', 'amount', 'vol', 'count']
    assert ExchangeUtil().fees(exchange='Binance') == 0.001


if __name__ == '__main__':
    test_exchangeUtil()