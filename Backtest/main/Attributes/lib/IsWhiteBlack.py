class IsWhiteBlack:

    def __init__(self, df, params):
        self.df = df
        self.attrName = params['attrName'] if 'attrName' in params.keys() else 'isWhiteBlack'
        self.whiteList = params['whiteList'] if 'whiteList' in params.keys() else []
        self.blackList = params['blackList'] if 'blackList' in params.keys() else []

    def isWhite(self, row):
        return row['close'] > row['open']

    def run(self):
        wBList = [False for _ in range(len(self.df))]
        for i in range(max(self.whiteList + self.blackList), len(self.df)):
            wBList[i] = False not in [self.isWhite(self.df.iloc[i-j]) for j in self.whiteList] and \
                        True not in [self.isWhite(self.df.iloc[i-j]) for j in self.blackList]
        return [(self.attrName, wBList)]
