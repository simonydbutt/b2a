from tinydb import Query


class UpdatePosition:

    def __init__(self, db):
        self.db = db

    def update(self, positionDict, currentPrice):
        self.db.update(
            {
                'currentPrice': currentPrice,
                'paperSize': round((currentPrice/positionDict['openPrice']) * positionDict['positionSize'],8),
                'periods': positionDict['periods'] + 1
            }, Query().assetName == positionDict['assetName']
        )
