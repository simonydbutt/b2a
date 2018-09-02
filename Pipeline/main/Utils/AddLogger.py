import Settings
import logging
from logging import handlers
import datetime
import time
import sys


class AddLogger:

    """
        *TODO: I think this is broken...
        *Add logging config
        https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
    """

    def __init__(self, stratName, db, fileLogLevel=logging.INFO, consoleLogLevel=logging.WARNING):
        self.filePath = '%s/Pipeline/DB/%s/%s/CodeLogs' % (Settings.BASE_PATH, db, stratName)
        dTime = datetime.datetime.fromtimestamp(round(time.time())).isoformat()
        logFormat = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        self.logger = logging.getLogger('')
        consoleLog = logging.StreamHandler(sys.stdout)
        consoleLog.setFormatter(logFormat)
        consoleLog.setLevel(consoleLogLevel)
        self.logger.addHandler(consoleLog)
        fileLog = handlers.RotatingFileHandler(
            '%s/%s_%s.log' % (self.filePath, stratName, dTime),
            maxBytes=(1048576*5), backupCount=7
        )
        fileLog.setFormatter(logFormat)
        fileLog.setLevel(fileLogLevel)
        self.logger.addHandler(fileLog)
