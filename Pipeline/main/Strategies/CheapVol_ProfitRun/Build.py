from Pipeline.main.Utils.SetupUtil import SetupUtil
from Pipeline.main.Finance.InitialSetup import InitialSetup as CapInit
from Pipeline.main.Strategies.CheapVol_ProfitRun.InitialSetup import InitialSetup as StratInit
import Settings


dbPath = '%s/Pipeline/DB' % Settings.BASE_PATH
SetupUtil().createDirStructure(dbPath=dbPath, baseStratName='CheapVol_ProfitRun')


# Setup capital files with initial capital £1000
CapInit(initialCapital=1000)

# Initially testing over timeframes: 1d, 12h, 6h, 2h
StratInit(
    gran='6h',
    CheapVolParams={
        'numPeriodsVolLong': 50,
        'numPeriodsVolShort': 5,
        'volCoef': 1.2,
        'numPeriodsMA': 30,
        'bolStd': 2
    },
    ProfitRunParams={
        'numPeriods': 50, 'closeAt': 50, 'stdDict': {'up': 1, 'down': 1.5}, 'maxRun': True
    }
)

