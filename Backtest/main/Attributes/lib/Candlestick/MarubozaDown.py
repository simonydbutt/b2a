class MarubozaDown:

    def __init__(self, df, params):
        self.df = df
        self.type = params['type'] if 'type' in params.keys() else 'full'
        self.attrName = params['attrName'] if 'attrName' in params.keys() else 'marubozaDown'
        self.coef = params['coef'] if 'coef' in params.keys() else 4

    def run(self):
        if self.type.lower() == 'ls':
            funct = self.lsMara
        elif self.type.lower() == 'us':
            funct = self.lsMara
        else:
            funct = self.fullMara
        self.df[self.attrName] = self.df.apply(funct, axis=1)
        return [(self.attrName, self.df[self.attrName])]

    def fullMara(self, row):
        return row['high'] == row['open'] and row['low'] == row['close']

    def lsMara(self, row):
        return row['high'] == row['open'] and self.coef * (row['close'] - row['low']) < row['open'] - row['close']

    def usMara(self, row):
        return row['low'] == row['close'] and self.coef * (row['high'] - row['open']) < row['open'] - row['close']
