class Doji:

    def __init__(self, df, params):
        self.df = df
        self.uCoef = params['uCoef'] if 'uCoef' in list(params.keys()) else 0.9
        self.dCoef = params['dCoef'] if 'dCoef' in list(params.keys()) else 0.9
        self.coef = params['coef'] if 'coef' in list(params.keys()) else 0.05
        self.type = params['type'] if 'type' in list(params.keys()) else 'longLeggedDoji'
        self.attrName = params['attrName'] if 'attrName' in list(params.keys()) else 'doji'
        self.dir = params['dir'] if 'dir' in list(params.keys()) else ''

    def run(self):
        if self.type == 'dragonfly':
            funct = self.dragonDoji
        elif self.type == 'gravestone':
            funct = self.graveStoneDoji
        else:
            funct = self.longLeggedDoji
        self.df[self.attrName] = self.df.apply(funct, axis=1)
        return [(self.attrName, self.df[self.attrName])]

    def longLeggedDoji(self, row):
        spread = row['high'] - row['low']
        if self.dir.lower() == 'up':
            return row['high'] - row['close'] >= self.uCoef/2.5 * spread and \
                row['close'] - row['low'] >= self.dCoef/2.5 * spread and \
                row['close'] - row['open'] < self.coef * spread
        elif self.dir.lower() == 'down':
            return row['high'] - row['open'] >= self.uCoef/2.5 * (row['open'] - row['close']) and \
                row['close'] - row['low'] >= self.dCoef/2.5 * spread and \
                row['open'] - row['close'] < self.coef * spread
        else:
            return row['high'] - max(row['open'], row['close']) >= self.uCoef/3 * spread and \
                min(row['open'], row['close']) - row['low'] >= self.dCoef/3 * spread and \
                abs(row['close'] - row['open']) < self.coef * spread

    def dragonDoji(self, row):
        spread = row['high'] - row['low']
        if self.dir.lower() == 'up':
            return row['high'] - row['close'] <= self.uCoef * spread and \
                row['close'] - row['low'] >= self.dCoef * spread and \
                row['close'] - row['open'] < self.coef * spread
        elif self.dir.lower() == 'down':
            return row['high'] - row['open'] <= self.uCoef * spread and \
                row['close'] - row['low'] >= self.dCoef * spread and \
                row['open'] - row['close'] < self.coef * spread
        else:
            return row['high'] - max(row['open'], row['close']) <= self.uCoef * spread and \
                min(row['open'], row['close']) - row['low'] >= self.dCoef * spread and \
                abs(row['close'] - row['open']) < self.coef * spread

    def graveStoneDoji(self, row):
        spread = row['high'] - row['low']
        if self.dir.lower() == 'up':
            return row['high'] - row['close'] >= self.uCoef * spread and \
                row['close'] - row['low'] <= self.dCoef * spread and \
                row['close'] - row['open'] < self.coef * spread
        elif self.dir.lower() == 'down':
            return row['high'] - row['open'] >= self.uCoef * spread and \
                row['close'] - row['low'] <= self.dCoef * spread and \
                row['open'] - row['close'] < self.coef * spread
        else:
            return row['high'] - max(row['open'], row['close']) >= self.uCoef * spread and \
                min(row['open'], row['close']) - row['low'] <= self.dCoef * spread and \
                abs(row['close'] - row['open']) < self.coef * spread