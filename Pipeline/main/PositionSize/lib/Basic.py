class Basic:

    """
        Simply returns percent of total liquid capital

        Config Requirements:
            - percent
    """

    def __init__(self, stratParams, capParams):
        self.capPercent = stratParams['percent'] if 'percent' in stratParams.keys() else .02
        self.liquidCap = capParams['liquidCurrent']

    def get(self, asset=None):
        return max(self.capPercent*self.liquidCap, 0.001)
