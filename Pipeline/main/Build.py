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
StratInit(
    gran='1d',
    CheapVolParams={
        'numPeriodsVolLong': 100,
        'numPeriodsVolShort': 5,
        'volCoef': 1.2,
        'numPeriodsMA': 50,
        'numStd': 1.5,
        'bolCoef': 1
    },
    ProfitRunParams={
        'numPeriods': 30,
        'closeAt': 40,
        'stdDict': {'up': 0.5, 'down': 1},
        'maxRun': True
    }
)
StratInit(
    gran='6h',
    CheapVolParams={
      'numPeriodsVolLong': 100,
      'numPeriodsVolShort': 5,
      'volCoef': 1.3,
      'numPeriodsMA': 30,
      'numStd': 2.5,
      'bolCoef': 1
    },
    ProfitRunParams={
        'numPeriods': 50,
        'closeAt': 50,
        'stdDict': {'up': 0.5, 'down': 1.5},
        'maxRun': True
    }
)
StratInit(
    gran='2h',
    CheapVolParams={
        'numPeriodsVolLong': 50,
        'numPeriodsVolShort': 5,
        'volCoef': 1.75,
        'numPeriodsMA': 60,
        'numStd': 2.5,
        'bolCoef': 1
    },
    ProfitRunParams={
        'numPeriods': 40,
        'closeAt': 40,
        'stdDict': {'up': 1.5, 'down': 2},
        'maxRun': True
    }
)

