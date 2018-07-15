class Hammer:

    def __init__(self, df, params):
        self.df = df
        self.coef = params['coef'] if 'coef' in params.keys() else 3
        self.attrName = params['attrName'] if 'attrName' in params.keys() else 'hammer'
        self.dir = params['dir'] if 'dir' in params.keys() else 'None'

    def run(self):
        self.df[self.attrName] = self.df.apply(self.isHammer, axis=1)
        return [(self.attrName, self.df[self.attrName])]

    def isHammer(self, row):
        if self.dir.lower() == 'up':
            return row['high'] == row['close'] and self.coef * (row['close'] - row['open']) < row['open'] - row['low']
        elif self.dir.lower() == 'down':
            return row['high'] == row['open'] and self.coef * (row['open'] - row['close']) < row['close'] - row['low']
        else:
            return row['high'] == max(row['open'], row['close']) and \
                   self.coef * abs(row['open'] - row['close']) < min(row['open'], row['close']) - row['low']