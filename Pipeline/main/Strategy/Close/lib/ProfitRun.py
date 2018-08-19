from Pipeline.main.PullData.Price.Pull import Pull
from tinydb import Query


class ProfitRun:
    """
        If config != hitPrice/sellPrice then calc as first run
        Trailing stop based on standard deviation levels.
        Sells if price goes below 'sellPrice'
        'sellPrice' increases is close > 'hitPrice'
    """

    def __init__(self, params, logger, isTest=False):
        self.isTest = isTest
        self.params = params['exit']
