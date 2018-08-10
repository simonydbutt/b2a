from Pipeline.main.Strategies.CheapVol_ProfitRun.RunStrat import RunStrat


RS = RunStrat(stratName='testStrat', dbPath='Pipeline/tests/testsDB')


def test_queryInOutPosition():
    assert RS.queryInOutPosition('LTCBTC')
    assert not RS.queryInOutPosition('XRPBTC')


if __name__ == '__main__':
    test_queryInOutPosition()
