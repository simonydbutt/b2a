import datetime
import time


class Utils:

    def date2Time(self, date, format="%Y-%m-%dT%H:%M:%S.000Z"):
            return time.mktime(datetime.datetime.strptime(date, format).timetuple())

