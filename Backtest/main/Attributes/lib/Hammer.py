class Hammer:

    def __init__(self, df, params):
        self.df = df
        self.coef = params['coef'] if 'coef' in list(params.keys()) else 5
        self.attrName = params['attrName'] if 'attrName' in list(params.keys()) else 'hammer'

    def run(self):
        self.df[self.attrName] = self.df.apply(self.isHammer, axis=1)
        return [(self.attrName, self.df[self.attrName])]

    def isHammer(self, row):
        return row['high'] == row['close'] and self.coef * (row['close'] - row['open']) < row['open'] - row['low']