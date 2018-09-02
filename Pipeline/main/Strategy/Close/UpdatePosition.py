from tinydb import Query


class UpdatePosition:

    def __init__(self, db):
        self.db = db

    def update(self, positionDict, currentPrice):
        self.db.update(
            {
                'currentPrice': currentPrice,
                'paperSize': (currentPrice/positionDict['openPrice']) * positionDict['positionSize'],
                'periods': positionDict['periods'] + 1
            }, Query().assetName == positionDict['assetName']
        )
