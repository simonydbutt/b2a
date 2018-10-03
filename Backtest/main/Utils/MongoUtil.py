from Backtest.main.Utils.TimeUtil import TimeUtil
from pymongo import MongoClient, DESCENDING, ASCENDING


class MongoUtil:

    """
        * insert_one/ query method is crazy slow when doing initial propagation but only a one time run and
        guarantees no duplication of data
    """

    def __init__(self, dbName):
        self.dbName = dbName
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[self.dbName]
        self.TU = TimeUtil()

    def toMongo(self, data, colName, id, parameters={}):
        for val in data:
            try:
                if len(list(self.db[colName].find({id: val[id]}))) == 0:
                    for param in parameters.keys():
                        if param == 'TS' and self.dbName == 'binance' or self.dbName == 'bitmex':
                            val['TS'] = int(self.TU.getTS(val[parameters['TS'][0]], timeFormat=parameters['TS'][1]))
                            self.db[colName].insert_one(val)
                        else:
                            try:
                                val[param] = val[parameters[param]]
                                self.db[colName].insert_one(val)
                            except TypeError:
                                print(val)
                                raise SystemExit
            except TypeError:
                print(val)
                print(list(self.db[colName].find({id: val[id]})))
                break

    def lastVal(self, colName):
        return list(self.db[colName].find({}, {'_id': 0, 'TS': 1}).sort('TS', DESCENDING).limit(1))[0]['TS']

    def count(self, colName):
        return self.db[colName].count()

    def index(self, colName):
        self.db[colName].ensure_index('TS', ASCENDING)
