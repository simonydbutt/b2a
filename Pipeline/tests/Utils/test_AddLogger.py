from Pipeline.tests.CreateCleanDir import CreateCleanDir
from Pipeline.main.Utils.AddLogger import AddLogger
import os
import logging
from contextlib import redirect_stdout
import io


CCD = CreateCleanDir(filePathList=['Pipeline/tests/test_DB/CodeLogs/testLogger'])


def test_fileLogging():
    CCD.create()
    consoleGrab = io.StringIO()
    with redirect_stdout(consoleGrab):
        AL = AddLogger(dirPath='Pipeline/tests/test_DB/CodeLogs/testLogger',
                       stratName='testStrat', consoleLogLevel=logging.WARNING,
                       fileLogLevel=logging.ERROR)
        AL.logger.error('Test Error')
        AL.logger.warning('Test Warning')
        AL.logger.info('Test Info')
    # list(filter(None, ...)) is to remove empty strings which aren't part of the logging
    logConsole = list(filter(None, consoleGrab.getvalue().split('\n')))
    file = os.listdir(AL.filePath)[0]
    with open('%s/%s' % (AL.filePath, file)) as f:
        logFile = list(filter(None, f.read().split('\n')))
    assert len(logConsole) == 2
    assert len(logFile) == 1
    CCD.clean()


if __name__ == '__main__':
    test_fileLogging()

