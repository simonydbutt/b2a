from Pipeline_.main.Strategies.CheapVol_ProfitRun.RunStrat import RunStrat
from tinydb import Query


RS = RunStrat(stratName='testStrat', dbPath='Pipeline_/tests/testsDB')


def test_queryInOutPosition():
    assert RS.queryInOutPosition('LTCBTC')
    assert not RS.queryInOutPosition('XRPBTC')


def test_updatePosition():
    RS.currentDB.update(
        {'periods': 0,
         'currentPrice': .00008107},
        Query().asset == 'LTCBTC'
    )
    RS.updatePosition(returnVal=3, asset='LTCBTC', close=.0001)
    val = RS.currentDB.search(Query().asset == 'LTCBTC')[0]
    assert val['currentPrice'] == .0001
    assert val['periods'] == 1
    RS.updatePosition(returnVal=2, asset='LTCBTC', close=.00008107)
    nVal = RS.currentDB.search(Query().asset == 'LTCBTC')[0]
    # Floating points...
    assert nVal['periods'] == 2
    assert abs(nVal['currentPrice'] - 0.00008107) < 1e-5
    assert abs(nVal['hitPrice'] - (0.00008107 + val['std'] * 1)) < 1e-8
    assert abs(nVal['sellPrice'] - (0.00008107 - val['std'] * .5)) < 1e-8


if __name__ == '__main__':
    test_queryInOutPosition()
    test_updatePosition()