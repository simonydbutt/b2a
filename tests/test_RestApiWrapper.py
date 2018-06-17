from PipeLine.main.RestApiWrapper import RestApiWrapper

RAW = RestApiWrapper()


def test_pullQuotes():
    l2Quotes = RAW.pullQuotes('XBTUSD')
    assert len(l2Quotes) == 2
    assert l2Quotes[0]['side'] == 'Sell'

def test_allXBTQuotes():
    data = RAW.allXBTQuotes()
    assert len(data.iloc[0]) == 6
