from Backtest.main.Utils.TimeUtil import TimeUtil
from pymongo import MongoClient, DESCENDING


class MongoUtil:

    def __init__(self, dbName):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[dbName]
        self.TU = TimeUtil()

    def toMongo(self, data, colName, id, parameters={}):
        for val in data:
            if len(list(self.db[colName].find({'timestamp': '2018-04-29T06:00:00.000Z'}))) == 0:
                for param in list(parameters.keys()):
                    if param == 'TS':
                        val['TS'] = int(self.TU.getTS(val[parameters['TS'][0]], timeFormat=parameters['TS'][1]))
                    else:
                        val[param] = parameters[param]
                self.db[colName].insert_one(val)

    def lastVal(self, colName):
        return list(self.db[colName].find({}, {'_id': 0, 'TS': 1}).sort('TS', DESCENDING).limit(1))[0]['TS']

    def count(self, colName):
        return self.db[colName].count()