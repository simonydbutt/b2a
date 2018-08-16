from Pipeline_.main.Finance.AnalyseOpenTrades import AnalyseOpenTrades


AOT = AnalyseOpenTrades(dbPath='Pipeline_/tests/testsDB/CurrentPositions')


def test_paperValue():

    assert AOT.paperValue() == 1.99


def test_allocated():
    assert AOT.allocated(liquidCurrent=100) == 0.0195


def test_numOpenTrades():
    assert AOT.numOpenTrades() == 4


if __name__ == '__main__':
    test_calc()
    test_allocated()
    test_numOpenTrades()