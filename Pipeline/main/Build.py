from Pipeline.main.Finance.InitialSetup import InitalSetup as CapInit
from Pipeline.main.Strategies.CheapVol_ProfitRun.InitialSetup import InitalSetup as StratInit
import Settings
import os


os.mkdir('%s/Pipeline/DB' % Settings.BASE_PATH)
os.mkdir('%s/Pipeline/DB/Configs' % Settings.BASE_PATH)
os.mkdir('%s/Pipeline/DB/CurrentPositions' % Settings.BASE_PATH)
os.mkdir('%s/Pipeline/DB/PerformanceLogs' % Settings.BASE_PATH)
os.mkdir('%s/Pipeline/DB/PerformanceLogs/StratLogs' % Settings.BASE_PATH)
os.mkdir('%s/Pipeline/DB/CodeLogs' % Settings.BASE_PATH)

# Setup capital files with initial capital £1000
CapInit(initialCapital=1000)

# Initially testing over timeframes: 1d, 12h, 6h, 2h
StratInit(gran='5m')
# StratInit(gran='12h')
# StratInit(gran='6h')
# StratInit(gran='2h')

