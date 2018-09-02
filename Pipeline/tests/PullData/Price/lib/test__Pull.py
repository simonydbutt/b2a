from Pipeline.tests.CreateCleanDir import CreateCleanDir
from Pipeline.main.PullData.Price.lib._Pull import _Pull
from Pipeline.main.Utils.AddLogger import AddLogger


CCD = CreateCleanDir(filePathList=['Pipeline/DB/test/CodeLogs'])


class TestReqSuccess:
    status_code = 200


class TestReqRateLimit:
    status_code = 429


class TestReqOtherFailure:
    status_code = 999


def test__pullData():
    CCD.create()
    AL = AddLogger(dirPath='Pipeline/DB/test/CodeLogs', stratName='test_Pull')
    P = _Pull(logger=AL.logger)
    assert P._pullData(endPoint='', isTest=True, testReq=TestReqSuccess) == 1
    assert P._pullData(endPoint='', isTest=True, testReq=TestReqRateLimit, testReq2=TestReqRateLimit) == 2
    assert P._pullData(endPoint='', isTest=True, testReq=TestReqRateLimit, testReq2=TestReqSuccess) == 3
    assert P._pullData(endPoint='', isTest=True, testReq=TestReqOtherFailure) == 4
    CCD.clean()


if __name__ == '__main__':
    test__pullData()