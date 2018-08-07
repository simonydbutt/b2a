from Backtest.main.Attributes.Attr import Attr
from Backtest.tests.resources.TestingLoad import testingLoad


def test_add(loc=None):
    df = testingLoad(loc=loc)
    A = Attr(df)
    df_ = A.add('TestAttr', params={'attrName': 'attrName'})
    assert df.iloc[-1]['open'] + df.iloc[-1]['close'] == df_.iloc[-1]['attrName1']
    assert df.iloc[0]['high'] + df.iloc[0]['low'] == df_.iloc[0]['attrName2']


if __name__ == '__main__':
    test_add(loc='../resources/')