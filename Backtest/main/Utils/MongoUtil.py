from Backtest.main.Utils.TimeUtil import TimeUtil
from pymongo import MongoClient, DESCENDING


class MongoUtil:

    def __init__(self, dbName):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[dbName]
        self.TU = TimeUtil()

    def toMongo(self, data, colName, id, parameters={}):
        for val in data:
            if len(list(self.db[colName].find({id: val[id]}))) == 0:
                for param in list(parameters.keys()):
                    if param == 'TS':
                        val['TS'] = int(self.TU.getTS(val[parameters['TS'][0]], timeFormat=parameters['TS'][1]))
                    else:
                        try:
                            val[param] = parameters[param]
                        except TypeError:
                            print(val)
                            raise SystemExit
                self.db[colName].insert_one(val)

    def lastVal(self, colName):
        return list(self.db[colName].find({}, {'_id': 0, 'TS': 1}).sort('TS', DESCENDING).limit(1))[0]['TS']

    def count(self, colName):
        return self.db[colName].count()

    def index(self, colName):
        return self.db[colName].create_index('TS')
