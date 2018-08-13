from Pipeline.main.Utils.SetupUtil import SetupUtil
from Pipeline.main.Strategies.CommitValue.InitialSetup import InitialSetup as StratInit
import Settings


dbPath = '%s/Pipeline/DB' % Settings.BASE_PATH
SetupUtil().createDirStructure(dbPath=dbPath, baseStratName='CommitValue')


StratInit()