class TestAttr:

    """
        Test Attr class
    """

    def __init__(self, df, params):
        self.df = df
        self.attrName = params['attrName'] if 'attrName' in params.keys() else 'TestAttr'

    def run(self):
        return [
            ('%s1' % self.attrName, self.df['open'] + self.df['close']),
            ('%s2' % self.attrName, self.df['high'] + self.df['low'])
        ]
