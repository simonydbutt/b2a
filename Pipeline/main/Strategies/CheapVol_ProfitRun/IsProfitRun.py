class IsProfitRun:

    def __init__(self, closeVal, stratParams, tradeParams):
        self.closeVal = closeVal
        self.tradeParams = tradeParams
        self.stratParams = stratParams

    def run(self):
        if self.tradeParams['periods'] == self.stratParams['closeAt']:
            return 0
        else:
            if self.closeVal < self.tradeParams['sellPrice']:
                return 1
            elif self.closeVal > self.tradeParams['hitPrice']:
                return 2
            else:
                return 3
