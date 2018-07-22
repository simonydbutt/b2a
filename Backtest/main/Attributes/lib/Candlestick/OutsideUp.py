import numpy as np


class OutsideUp:

    def __init__(self, df, params):
        self.df = df
        self.attrName = params['attrName'] if 'attrName' in params.keys() else 'outsideUp'
        self.delay = params['delay'] if 'delay' in params.keys() else 1
        self.bullConfirm = params['bullConf'] if 'bullConf' in params.keys() else True
        self.coef = params['coef'] if 'coef' in params.keys() else 1.5

    def run(self):
        oUList = [False for _ in range(len(self.df))]
        initMax = [np.NaN for _ in range(1 + self.delay)]
        for i_ in range(1 + self.delay, len(self.df)):
            i = i_ - self.delay
            initRow = self.df.iloc[i - 1]
            initRange = initRow['open'] - initRow['close']
            if initRange > 0:
                row = self.df.iloc[i]
                rowRange = row['close'] - row['open']
                initMax.append(max(row['close'], initRow['open']))
                if rowRange > 0 and row['open'] < initRow['close'] and \
                        row['close'] > initRow['open'] and rowRange > self.coef*initRange:
                    oUList[i_] = True
            else:
                initMax.append(np.NaN)
        if not self.bullConfirm:
            return [(self.attrName, oUList)]
        else:
            return [
                (self.attrName, oUList),
                ('bullConf', initMax)
            ]