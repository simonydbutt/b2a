class Doji:

    def __init__(self, df, params):
        self.df = df
        self.uCoef = params['uCoef'] if 'uCoef' in list(params.keys()) else 10
        self.dCoef = params['dCoef'] if 'dCoef' in list(params.keys()) else 10
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
        for field in ['high', 'low', 'close', 'open']:
            row[field] = float(row[field])
        if self.dir.lower() == 'up':
            return row['high'] - row['close'] >= self.uCoef * (row['close'] - row['open']) and \
                row['close'] - row['low'] >= self.dCoef * (row['close'] - row['open']) and \
                row['open'] >= row['close']
        elif self.dir.lower() == 'down':
            return row['high'] - row['open'] >= self.uCoef * (row['open'] - row['close']) and \
                row['close'] - row['low'] >= self.dCoef * (row['open'] - row['close']) and \
                row['open'] <= row['close']
        else:
            return row['high'] - max(row['open'], row['close']) >= self.uCoef * abs(row['open'] - row['close']) and \
                min(row['open'], row['close']) - row['low'] >= self.dCoef * abs(row['open'] - row['close'])

    def dragonDoji(self, row):
        for field in ['high', 'low', 'close', 'open']:
            row[field] = float(row[field])
        if self.dir.lower() == 'up':
            return row['high'] - row['close'] <= self.uCoef * (row['close'] - row['open']) and \
                row['close'] - row['low'] >= self.dCoef * (row['close'] - row['open']) and \
                row['open'] >= row['close']
        elif self.dir.lower() == 'down':
            return row['high'] - row['open'] <= self.uCoef * (row['open'] - row['close']) and \
                row['close'] - row['low'] >= self.dCoef * (row['open'] - row['close']) and \
                row['open'] <= row['close']
        else:
            return row['high'] - max(row['open'], row['close']) <= self.uCoef * abs(row['open'] - row['close']) and \
                min(row['open'], row['close']) - row['low'] >= self.dCoef * abs(row['open'] - row['close'])

    def graveStoneDoji(self, row):
        for field in ['high', 'low', 'close', 'open']:
            row[field] = float(row[field])
        if self.dir.lower() == 'up':
            return row['high'] - row['close'] >= self.uCoef * (row['close'] - row['open']) and \
                row['close'] - row['low'] <= self.dCoef * (row['close'] - row['open']) and \
                row['open'] >= row['close']
        elif self.dir.lower() == 'down':
            return row['high'] - row['open'] >= self.uCoef * (row['open'] - row['close']) and \
                row['close'] - row['low'] <= self.dCoef * (row['open'] - row['close']) and \
                row['open'] <= row['close']
        else:
            return row['high'] - max(row['open'], row['close']) >= self.uCoef * abs(row['open'] - row['close']) and \
                min(row['open'], row['close']) - row['low'] <= self.dCoef * abs(row['open'] - row['close'])