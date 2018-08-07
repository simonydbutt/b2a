from Pipeline.main.Finance.PaperGains import PaperGains


PG = PaperGains(fees=0.01, dbPath='Pipeline/tests/testsDB/CurrentPositions')


def test_calc():
    assert PG.calc() == 264.64
    print('Tested paper gains calc')

def test_allocated():
    assert PG.allocated(liquidCurrent=100) == 0.7258

if __name__ == '__main__':
    test_calc()
    test_allocated()