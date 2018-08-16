from Pipeline_.main.Utils.SetupUtil import SetupUtil
from Pipeline_.main.Strategies.CommitValue.InitialSetup import InitialSetup as StratInit
import Settings


dbPath = '%s/Pipeline_/DB' % Settings.BASE_PATH
SetupUtil().createDirStructure(dbPath=dbPath, baseStratName='CommitValue')


StratInit()