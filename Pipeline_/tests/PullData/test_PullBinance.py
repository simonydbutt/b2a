# from Pipeline_.main.PullData.PullBinance import PullBinance
# import time
#
# """
#     Tests binance connection and makes sure time is in sync
#     * Assumes time sync within 10 seconds is okay
# """
#
#
# PB = PullBinance()
#
#
# def test_connection():
#     assert PB._pullData('/api/v1/ping') == {}
#     assert round(PB._pullData('/api/v1/time')['serverTime']/10000) == round(time.time()/10)
#
# def test_getCandles():
#     data = PB.getCandles('ETHBTC', 5, '1d')
#     assert len(data) == 5
#     assert list(data) == ['TS', 'open', 'high', 'low', 'close', 'takerQuoteVol']
#
#
# if __name__ == '__main__':
#     test_connection()
#     test_getCandles()