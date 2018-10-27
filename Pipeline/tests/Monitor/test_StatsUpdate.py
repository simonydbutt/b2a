from Pipeline.main.Monitor.StatsUpdate import StatsUpdate
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from pandas.util.testing import assert_frame_equal
from pymongo import MongoClient
import pandas as pd
import Settings
import logging
import yaml


client = MongoClient("localhost", 27017)
dbPath = "Pipeline/resources"
CCD = CreateCleanDir(["%s/testStrat1" % dbPath, "%s/testStrat2" % dbPath])
dummy_positions = [
    {
        "assetName": "ETHBTC",
        "openPrice": 0.0000158,
        "currentPrice": 10,
        "periods": 0,
        "hitPrice": 11,
        "positionSize": 0.4995,
        "paperSize": 0.4995,
        "TSOpen": 1534711395,
        "sellPrice": 9,
        "exchange": "Binance",
    },
    {
        "assetName": "LTCBTC",
        "openPrice": 0.0000158,
        "currentPrice": 0.0000158,
        "periods": 6,
        "sellPrice": 9,
        "positionSize": 0.4995,
        "paperSize": 0.4995,
        "TSOpen": 1534711395,
        "hitPrice": 11,
        "exchange": "Binance",
    },
]
currentStatsDF = pd.DataFrame(
    [
        ["ETHBTC", 10, 0.0000158, 0, 63291139.2405],
        ["LTCBTC", 0.0000158, 0.0000158, 0.12, 100],
    ],
    columns=["assetName", "currentPrice", "openPrice", "daysOpen", "%"],
)
currentEmptyStats = pd.DataFrame(
    [], columns=["assetName", "currentPrice", "openPrice", "daysOpen", "%"]
)


def before():
    compPath = "%s/%s" % (Settings.BASE_PATH, dbPath)
    after()
    CCD.create()
    for strat in ("testStrat1", "testStrat2"):
        colDB = client[strat]["currentPositions"]
        colDB.insert_many(dummy_positions)
        transDB = client[strat]["transactionLogs"]
        transDB.insert_many([{"a": 1}, {"b": 2}, {"c": 2}])
        capitalDict = {
            "initialCapital": 10,
            "liquidCurrent": 9,
            "paperCurrent": 11,
            "paperPnL": 0.1,
            "percentAllocated": 0.1,
        }
        with open("%s/%s/capital.yml" % (compPath, strat), "w") as capFile:
            yaml.dump(capitalDict, capFile)


def after():
    CCD.clean()
    for strat in ["testStrat1", "testStrat2"]:
        client.drop_database(strat)


def test_indivStats():
    before()
    SU = StatsUpdate()
    stats = SU.indivStats("testStrat1")
    assert stats["initialCapital"] == 10
    assert stats["numberOpen"] == 2
    assert stats["numberTransactions"] == 3
    assert stats["openList"] == ["ETHBTC", "LTCBTC"]
    assert stats["paperAvgPnL"] == 0.02
    after()


def test_compStats():
    before()
    SU = StatsUpdate()
    statDict = SU.compStats(isTest=["testStrat1", "testStrat2"])
    assert len(list(statDict)) == 3
    totDict = statDict["total"]
    assert totDict["numberOpen"] == 4
    assert totDict["initialCapital"] == 20
    assert totDict["liquidCurrent"] == 18
    assert totDict["paperCurrent"] == 22
    assert totDict["percentAllocated"] == 18
    after()


def test_getCurrentStats():
    before()
    df = StatsUpdate().getCurrentStats(stratName="testStrat1")
    assert_frame_equal(df, currentStatsDF)
    client.testStrat1.drop_collection("currentPositions")
    df = StatsUpdate().getCurrentStats(stratName="testStrat1")
    assert_frame_equal(df, currentEmptyStats)
    after()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    try:
        test_indivStats()
        test_compStats()
        test_getCurrentStats()
    except AssertionError:
        after()
        raise AssertionError
