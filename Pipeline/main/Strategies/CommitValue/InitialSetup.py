from Pipeline.main.Utils.SetupUtil import SetupUtil
import uuid


class InitialSetup:

    def __init__(self, minCommits=300, numPositions=10, stratName='CommitValue',
                 exchangeList=('Binance', 'HitBTC', 'Hadax')):
        self.stratID = str(uuid.uuid4())
        self.configDict = {
            'minCommits': minCommits,
            'numPositions': numPositions,
            'exchanges': exchangeList,
            'performance': {
                'percentPnL': 0,
                'maxGain': 0,
                'maxLoss': 0,
                'numPeriods': 0,
                'winLoss': 0,
                'numTrades': 0
            },
            'stratID': self.stratID
        }
        SetupUtil().createConfigs(configDict=self.configDict, baseStrat=stratName, stratName=stratName)
