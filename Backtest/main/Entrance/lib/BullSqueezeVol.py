from Backtest.main.Attributes.Attr import Attr
import numpy as np


class BullSqueezeVol:

    """
        MA50 > MA10
        Bull squeeze pattern
        Vol for init > Mean(Vol_20) + std
        Vol for last squeeze period + 1 < Mean(Vol_20)
        Squeeze +1 white
    """

    def __init__(self, df, params):
        self.numBSPeriods = params['numBSPeriods'] if 'numBSPeriods' in params.keys() else 3
        self.maLong = params['maLong'] if 'maLong' in params.keys() else 50
        self.maShort = params['maShort'] if 'maShort' in params.keys() else 10
        self.volPeriods = params['volPeriods'] if 'volPeriods' in params.keys() else 40
        self.condList = params['condList'] if 'condList' in params.keys() else ('isWhite', 'maBelow', 'volCond')
        self.df = Attr(
            Attr(
                Attr(
                    Attr(
                        Attr(df).add('MA', params={'numPeriods': self.volPeriods, 'col': 'takerBaseAssetVol',
                                                   'attrName': 'meanVol'})
                    ).add('Bollinger', params={'maField': 'meanVol', 'numStd': .5, 'attrName': 'bolVol'})
                ).add('MA', params={'numPeriods': self.maLong, 'attrName': 'maLong'})
            ).add('MA', params={'numPeriods': self.maShort, 'attrName': 'maShort'})
        ).add('BullSqueeze', params={'numPeriods': self.numBSPeriods, 'delay': 1})
        self.df['isWhite'] = self.df['close'] > self.df['open']
        self.df['maBelow'] = self.df['maLong'] > self.df['maShort']
        self.runStats = {}

    def run(self):
        self.df['volCond'] = self.volCond()
        self.df['bullSqueezeVol'] = self.df.apply(self.conditions, axis=1)
        for cond in ['bullSqueeze', 'isWhite', 'maBelow', 'volCond']:
            self.runStats[cond] = round(sum(self.df[cond])/len(self.df), 4)
        print(self.runStats)
        return list(self.df[self.df['bullSqueezeVol']]['TS'].values)

    def conditions(self, row):
        return False not in [row[val] for val in self.condList] + [row['bullSqueeze']]

    def volCond(self):
        volList = [False for _ in range(len(self.df))]
        for i in range(self.numBSPeriods, len(self.df)):
            row = self.df.iloc[i]
            if self.df.iloc[i-self.numBSPeriods-1]['takerBaseAssetVol'] > row['bolVolUp'] and \
                    row['takerBaseAssetVol'] < (row['meanVol'] + row['bolVolUp'])/2:
                volList[i] = True
        return volList
