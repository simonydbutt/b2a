from Backtest.main.Attributes.Attr import Attr
from Backtest.main.Data.Load import Load


class ResistanceLoss:

    """
        Take loss when close < resistance10
        Take profit when openT < close < MA3
    """

    def __init__(self, df, params, enterList):
        self.numMAPeriods = params['numMAPeriods'] if 'numMAPeriods' in params.keys() else 3
        self.numRPeriods = params['numRPeriods'] if 'numRPeriods' in params.keys() else 3
        self.coef = params['coef'] if 'coef' in params.keys() else 0.98
        self.df = Attr(
            Attr(df).add('MA', params={'attrName': 'exitMA', 'numPeriods': self.numMAPeriods})
        ).add('Support', params={'numPeriods': self.numRPeriods})
        self.enterList = enterList

    def getIndex(self, df, TSVal):
        return df.index[df['TS'] == TSVal].tolist()[0]

    def run(self):
        positionList = []
        for val in self.enterList:
            pos = self.getIndex(self.df, val)
            buyAt = self.df.iloc[pos]['close']
            # print('\n%s' % buyAt)
            periods = 1
            while periods < 50:
                row = self.df.iloc[pos + periods]
                if row['close'] < row['support']:
                    # print(1)
                    # print(row['support'])
                    # print(row['close'])
                    break
                elif row['close'] < self.coef*row['exitMA'] or row['close'] > buyAt:
                    # print(2)
                    # print(row['close'])
                    # print(row['exitMA'])
                    break
                else:
                    periods += 1
            positionList.append((pos, pos + periods))
        return positionList


# df = Load(dbName='binance').loadOne('XMRBTC_2h', timeStart=1483228800, timeEnd=1527811200)
# enterList = [1513324800.0, 1514304000.0, 1514764800.0, 1515139200.0]
#
# R = ResistanceLoss(df=df, enterList=enterList, params={'numMAPeriods': 5, 'numRPeriods': 10, 'coef': 0.95})
# print(R.run())