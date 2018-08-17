class Basic:

    """
        Simply returns percent of total liquid capital
    """

    def __init__(self, stratParams, capParams):
        self.capPercent = stratParams['percent'] if 'percent' in stratParams.keys() else .02
        self.liquidCap = capParams['liquidCurrent']

    def get(self, asset=None):
        return self.capPercent*self.liquidCap
