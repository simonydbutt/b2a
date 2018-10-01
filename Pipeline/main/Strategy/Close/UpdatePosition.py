from pymongo import MongoClient
import logging


class UpdatePosition:

    def __init__(self, stratName):
        logging.debug('Initialising UpdatePosition()')
        self.col = MongoClient('localhost', 27017)[stratName]['currentPositions']

    def update(self, positionDict, currentPrice):
        logging.debug('Starting UpdatePosition.update')
        positionDict['periods'] += 1
        positionDict['paperSize'] = round(float(positionDict['positionSize'])*float(currentPrice)/float(positionDict['openPrice']), 8)
        positionDict['currentPrice'] = currentPrice
        positionDict.pop('_id', None)
        logging.debug('New vals: periods: %s, paperSize: %s, currentPrice: %s' %
                      (positionDict['periods'], positionDict['paperSize'], positionDict['currentPrice']))
        self.col.find_one_and_replace({'assetName': positionDict['assetName']}, positionDict)
        logging.debug('Ending UpdatePosition.update')
