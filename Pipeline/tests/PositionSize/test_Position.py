from Pipeline.main.PositionSize.Position import Position


def test_Positon():
    P = Position(stratFilePath='Pipeline/tests/test_DB/Configs/testStrat.yml',
                 capFilePath='Pipeline/tests/test_DB',
                 capFileName='Capital.yml')
    assert P.getSize() == 0.45


if __name__ == '__main__':
    test_Positon()