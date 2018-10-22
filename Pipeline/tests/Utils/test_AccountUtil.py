from Pipeline.main.Utils.AccountUtil import AccountUtil
import logging

accountDet = {"BTC": 7, "ETH": 20, "LTC": 100}
isTest = {"ETH": 0.1, "LTC": 0.01}


def test_calcValue():
    assert AccountUtil("testExchange", isTest=isTest)._calcValue(accountDet) == 3


def test_getValue():
    capDict = AccountUtil("testExchange", isTest=isTest).getValue(
        initCapital=15, isTest=accountDet
    )
    assert capDict["initialCapital"] == 15
    assert capDict["liquidCurrent"] == 7
    assert capDict["paperCurrent"] == 10
    assert capDict["paperPnL"] == 0.67
    assert capDict["percentAllocated"] == 0.3


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    test_calcValue()
    test_getValue()
