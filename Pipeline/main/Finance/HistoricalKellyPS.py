class HistoricalKellyPS:

    """
        Basic kelly criterion position sizing based on historical advantage
        got from backtesting and sandbox
    """

    def __init__(self, stratParams):
        self.stratParams = stratParams

    def positionSize(self, liquidCapital):
        return round(self.stratParams['kelly']['coef'] * self.stratParams['kelly']['adv'] * liquidCapital, 3)