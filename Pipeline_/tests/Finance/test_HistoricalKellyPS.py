from Pipeline_.main.Finance.HistoricalKellyPS import HistoricalKellyPS as HK


def test_positionSize():
    assert HK(stratParams={
        'kelly': {
            'coef': 1,
            'adv': 0.05
        }}).positionSize(liquidCapital=1000) == 50
    assert HK(stratParams={
        'kelly': {
            'coef': 0.05,
            'adv': 0.05
        }}).positionSize(985) == 2.463

