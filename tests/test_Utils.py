from b2b.main.Utils import Utils

U = Utils()


def test_date2Time():
    assert U.date2Time("2018-06-16T7:53:00.000Z") == 1529131980.0
    assert U.date2Time("2018/06/16", format="%Y/%m/%d") == 1529103600
