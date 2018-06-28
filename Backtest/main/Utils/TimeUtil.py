import time
from datetime import datetime


class TimeUtil:

    def getTS(self, date, timeFormat='%Y-%m-%dT%H:%M:%S.000Z'):
        return time.mktime(datetime.strptime(date, timeFormat).timetuple())

    def getDatetime(self, timestamp, timeFormat='%Y-%m-%dT%H:%M:%S.000Z'):
        return datetime.fromtimestamp(int(timestamp)).strftime(timeFormat)
