import time
from datetime import datetime


class TimeUtil:

    def __init__(self):
        self.bin2TS = {
            '1w': 7 * 24 * 60 * 60, '3d': 3 * 24 * 60 * 60, '1d': 24 * 60 * 60,
            '12h': 12 * 60 * 60, '6h': 6 * 60 * 60, '4h': 4*60*60,
            '2h': 2 * 60 * 60, '1h': 60 * 60 , '30m': 30 * 60#, '15m': 15 * 60,
            #'5m': 60, '1m': 5 * 60,
        }
        self.ts2Bin = {
            '604800': '1w', '259200': '3d', '86400': '1d',
            '43200': '12h', '21600': '6h', '14400': '4h',
            '7200': '2h', '3600': '1h', '1800': '30m' #, '900'; '15m',
            #'300': '5m', '60': '1m'
        }

    def getTS(self, date, timeFormat='%Y-%m-%dT%H:%M:%S.000Z'):
        return time.mktime(datetime.strptime(date, timeFormat).timetuple())

    def getDatetime(self, timestamp, timeFormat='%Y-%m-%dT%H:%M:%S.000Z'):
        return datetime.fromtimestamp(int(timestamp)).strftime(timeFormat)
