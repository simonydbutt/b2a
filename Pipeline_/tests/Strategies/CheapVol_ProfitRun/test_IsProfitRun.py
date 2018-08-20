# from Pipeline_.main.Strategies.CheapVol_ProfitRun.IsProfitRun import IsProfitRun as IPR
#
#
# def test_IsProfitRun():
#     assert IPR(closeVal=10, stratParams={'closeAt': 10},
#                tradeParams={'sellPrice': 9.5, 'hitPrice': 10, 'periods': 1}).run() == 3
#     assert IPR(closeVal=10, stratParams={'closeAt': 10},
#                tradeParams={'sellPrice': 8, 'hitPrice': 9, 'periods': 1}).run() == 2
#     assert IPR(closeVal=10, stratParams={'closeAt': 10},
#                tradeParams={'sellPrice': 11, 'hitPrice': 15, 'periods': 1}).run() == 1
#     assert IPR(closeVal=10, stratParams={'closeAt': 10},
#                tradeParams={'sellPrice': 11, 'hitPrice': 15, 'periods': 11}).run() == 0
#
