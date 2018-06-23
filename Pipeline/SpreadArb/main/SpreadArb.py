from Pipeline.SpreadArb.main.RestApiWrapper import RestApiWrapper
import json
import pandas as pd


class SpreadArb:

    def __init__(self, verbose=False, assets=('PM', 'PU', 'UM'), libPath='./lib/'):
        self.libPath = libPath
        self.assets = assets
        self.verbose = verbose
        with open(self.libPath + 'hyperParam.json') as hPFile:
            self.hyperParam = json.load(hPFile)
        with open(self.libPath + 'tmpVals.json') as tmpFile:
            self.tmpVals = json.load(tmpFile)
        with open(self.libPath + 'capital.json') as cFile:
            self.capital = json.load(cFile)
        self.latest = RestApiWrapper().allXBTQuotes()
        self.tradeLog = []
        if self.verbose:
            print('Run start')

    def _resetTmp(self):
        return {
            "inPosition": False,
            "pairing": -1,
            "tmpLong": -1,
            "tmpShort": -1,
            "tmpSpread": -1,
            "longVal": -1,
            "numPeriods": -1,
            "maxDrawDown": 0,
            "positionSize": -1
        }

    def run(self):
        if not self.tmpVals['inPosition']:
            self.isEnter()
        else:
            self.isExit()
        self.closeUp()

    def isEnter(self):
        i = 0
        while i < len(self.assets):
            pair = self.assets[i]
            i += 1
            # If spread becomes greater than 3% bitcoin price -> Enter
            if self.latest['spread%s' % pair].iloc[0] > self.hyperParam['spreadEnter']*self.latest[pair[0]].iloc[0] and\
                self.latest['spread%s' % pair].iloc[0] < (self.hyperParam['spreadExitL'] - 0.005)*self.latest[pair[0]].iloc[0]:
                self.tmpVals['inPosition'] = True
                self.tmpVals['pairing'] = pair
                self.tmpVals['tmpSpread'] = self.latest['spread%s' % pair].iloc[0]
                if self.latest[pair[0]].iloc[0] > self.latest[pair[1]].iloc[0]:
                    self.tmpVals['tmpLong'] = self.latest[pair[1]].iloc[0]
                    self.tmpVals['tmpShort'] = self.latest[pair[0]].iloc[0]
                    self.tmpVals['longVal'] = 1
                else:
                    self.tmpVals['tmpLong'] = self.latest[pair[0]].iloc[0]
                    self.tmpVals['tmpShort'] = self.latest[pair[1]].iloc[0]
                    self.tmpVals['longVal'] = 0
                self.tmpVals['numPeriods'] = 0
                if self.verbose:
                    print('Enter position %s, Long: %s, Short: %s, with initial spread: %s' %
                          (pair, pair[self.tmpVals['longVal']], pair[1-self.tmpVals['longVal']],
                           self.latest['spread%s' % pair]))
                self.placeTrade()
                break
            elif self.verbose:
                print('Spread not large enough for pair: %s\nRequired: %s, Actual: %s' %
                      (pair, round(self.hyperParam['spreadEnter']*self.latest[pair[0]].iloc[0]),
                       self.latest['spread%s' % pair].iloc[0]))

    def isExit(self):
        # If spread becomes less than 0.5% bitcoin price -> Exit w. profit
        # If spread becomes greater than 5% bitcoin price -> Exit w. loss
        if self.latest['spread%s' % self.tmpVals['pairing']].iloc[0] < self.hyperParam['spreadExitP']*self.latest[self.tmpVals['pairing'][0]].iloc[0] \
                or self.latest['spread%s' % self.tmpVals['pairing']].iloc[0] > self.hyperParam['spreadExitL']*self.latest[self.tmpVals['pairing'][0]].iloc[0]:
            pL = self.updateBook(isClose=True)
            self.tradeLog = [pL, self.tmpVals['maxDrawDown'], self.tmpVals['numPeriods']]
            self.tmpVals = self._resetTmp()
        else:
            self.tmpVals['numPeriods'] += 1
            tmpPL = self.latest['spread%s' % self.tmpVals['pairing']].iloc[0] - self.tmpVals['tmpSpread']
            if self.verbose: print(tmpPL)
            if tmpPL < self.tmpVals['maxDrawDown']:
                self.tmpVals['maxDramDown'] = tmpPL

    def positionSize(self):
        # Basic atm, add to later
        position = round(0.25 * (self.capital['total'] - self.capital['illiquid'])) * self.hyperParam['leverage']
        return position, position

    def placeTrade(self):
        # Function to place trade on Bitmex
        # TODO
        longPosition, shortPosition = self.positionSize()
        self.updateBook(longPosition, shortPosition)

    def updateBook(self, longPosition=None, shortPosition=None, isClose=False):
        if not isClose:
            print(longPosition)
            print(shortPosition)
            self.tmpVals['positionLong'] = (1-self.hyperParam['takerFee']) * longPosition
            self.tmpVals['positionShort'] = (1-self.hyperParam['takerFee']) * shortPosition
            self.capital['illiquid'] += (1-self.hyperParam['takerFee']) * (longPosition + shortPosition)/self.hyperParam['leverage']
        else:
            self.capital['illiquid'] = 0
            longSide = (self.tmpVals['positionLong'] * (1-self.hyperParam['takerFee'])) * \
                       (self.latest[self.tmpVals['pairing'][self.tmpVals['longVal']]].iloc[0] / self.tmpVals['tmpLong'])
            shortSide = (self.tmpVals['positionShort'] * (1 - self.hyperParam['takerFee'])) * \
                        (self.tmpVals['tmpShort'] / self.latest[self.tmpVals['pairing'][1 - self.tmpVals['longVal']]].iloc[0])
            pL = longSide + shortSide - self.tmpVals['positionShort'] - self.tmpVals['positionLong']
            self.capital['total'] += round(pL, 4)
            return pL

    def closeUp(self):
        with open(self.libPath + 'tmpVals.json', 'w') as outfile:
            json.dump(self.tmpVals, outfile)
        with open(self.libPath + 'capital.json', 'w') as cFile:
            json.dump(self.capital, cFile)
        if len(self.tradeLog) != 0:
            closeDF = pd.DataFrame([self.tradeLog], columns=['P&L', 'MaxDrawdown', 'Periods'])
            if self.verbose: print(closeDF)
            try:
                df = pd.read_feather(self.libPath + 'positionLog')
                df = df.append(closeDF)
            except IOError:
                df = closeDF
            df.reset_index(drop=True).to_feather(self.libPath + 'positionLog')
        if self.verbose: print('Run complete')