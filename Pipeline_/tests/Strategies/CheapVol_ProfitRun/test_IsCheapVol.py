from Pipeline_.main.Strategies.CheapVol_ProfitRun.IsCheapVol import IsCheapVol
import pandas as pd


def test_IsCheapVol():
    df = pd.DataFrame(
        [[1.533341e+09, 0.054550, 0.056501, 0.054200, 0.056334, 3827.066703],
         [1.533427e+09, 0.056335, 0.058597, 0.055767, 0.058060, 3989.376136],
         [1.533514e+09, 0.058064, 0.058550, 0.057664, 0.058160, 2879.807693],
         [1.533600e+09, 0.058160, 0.058700, 0.057658, 0.058400, 3473.632801],
         [1.533686e+09, 0.058400, 0.058650, 0.055749, 0.055970, 3593.550686]],
        columns=['TS', 'open', 'high', 'low', 'close', 'takerQuoteVol'])

    CV1 = IsCheapVol(df, params={
        'numPeriodsVolLong': 5,
        'numPeriodsVolShort': 2,
        'numPeriodsMA': 3,
        'bolStd': -1,
        'volCoef': 0.5
    })
    CV2 = IsCheapVol(df, params={
        'numPeriodsVolLong': 5,
        'numPeriodsVolShort': 2,
        'numPeriodsMA': 3,
        'bolStd': -1,
        'volCoef': 2
    })
    CV3 = IsCheapVol(df, params={
        'numPeriodsVolLong': 5,
        'numPeriodsVolShort': 2,
        'numPeriodsMA': 3,
        'bolStd': 2,
        'volCoef': 0.5
    })
    assert CV1.run()
    assert not CV2.run()
    assert not CV3.run()

