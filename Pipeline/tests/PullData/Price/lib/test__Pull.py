from Pipeline.tests.CreateCleanDir import CreateCleanDir
from Pipeline.main.PullData.Price.lib._Pull import _Pull
import logging


class TestReqSuccess:
    status_code = 200


class TestReqRateLimit:
    status_code = 429


class TestReqOtherFailure:
    status_code = 999


def test__pullData():
    P = _Pull()
    assert P._pullData(endPoint="", isTest=True, testReq=TestReqSuccess) == 1
    assert (
        P._pullData(
            endPoint="",
            isTest=True,
            testReq=TestReqRateLimit,
            testReq2=TestReqRateLimit,
        )
        == 2
    )
    assert (
        P._pullData(
            endPoint="", isTest=True, testReq=TestReqRateLimit, testReq2=TestReqSuccess
        )
        == 3
    )
    assert P._pullData(endPoint="", isTest=True, testReq=TestReqOtherFailure) == 4


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    test__pullData()
