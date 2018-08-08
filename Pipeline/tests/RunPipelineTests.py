from Pipeline.tests.Audit.test_DailyCapital import *
from Pipeline.tests.Finance.test_HistoricalKellyPS import *
from Pipeline.tests.Finance.test_PaperGains import *
from Pipeline.tests.PullData.test_PullBinance import *
from Pipeline.tests.Strategies.CheapVol_ProfitRun.test_IsProfitRun import *
from Pipeline.tests.Strategies.CheapVol_ProfitRun.test_IsCheapVol import *


class RunPipelineTests:

    def __init__(self):
        test_DailyCapital()
        print('Daily capital logging working')
        test_positionSize()
        print('Tested kelly position sizing')
        test_calc()
        test_allocated()
        print('Tested paper gains')
        test_connection()
        test_getCandles()
        print('Tested Binance connection')
        test_IsCheapVol()
        print('IsCheapVol working')
        test_IsProfitRun()
        print('IsProfitRun working')
        print('Initial pipeline tests complete!\n')
