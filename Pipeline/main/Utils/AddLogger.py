import logging
from logging import handlers
import datetime
import time
import sys


class AddLogger:

    def __init__(self, filePath, stratName, fileLogLevel=logging.INFO, consoleLogLevel=logging.WARNING):
        dTime = datetime.datetime.fromtimestamp(round(time.time())).isoformat()
        self.logger = logging.getLogger('')
        self.logger.setLevel(consoleLogLevel)
        consoleLog = logging.StreamHandler(sys.stdout)
        consoleLog.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))
        self.logger.addHandler(consoleLog)
        fileLogFormat = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        fileLog = handlers.RotatingFileHandler('%s/%s_%s.log' % (filePath, stratName, dTime),
                                            maxBytes=(1048576*5), backupCount=7)
        fileLog.setFormatter(fileLogFormat)
        fileLog.setLevel(fileLogLevel)
        self.logger.addHandler(fileLog)
