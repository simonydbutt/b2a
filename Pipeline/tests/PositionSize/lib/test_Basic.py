from Pipeline.main.PositionSize.lib.Basic import Basic


def test_Basic():
    assert Basic(stratParams={'percent': 0.05}, capParams={'liquidCurrent': 1000}).get() == 50
    assert Basic(stratParams={}, capParams={'liquidCurrent': 100}).get() == 2


if __name__ == '__main__':
    test_Basic()