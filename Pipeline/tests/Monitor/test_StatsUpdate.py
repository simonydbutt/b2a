from Pipeline.main.Monitor.StatsUpdate import StatsUpdate
from Pipeline.tests.CreateCleanDir import CreateCleanDir
from pymongo import MongoClient
import Settings
import yaml


client = MongoClient("localhost", 27017)
dbPath = "Pipeline/resources"
CCD = CreateCleanDir(["%s/testStrat1" % dbPath, "%s/testStrat2" % dbPath])


def before():
    compPath = "%s/%s" % (Settings.BASE_PATH, dbPath)
    after()
    CCD.create()
    for strat in ("testStrat1", "testStrat2"):
        colDB = client[strat]["currentPositions"]
        colDB.insert_one({"assetName": "LTCBTC"})
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
    assert stats["numberOpen"] == 1
    assert stats["numberTransactions"] == 3
    assert stats["openList"] == ["LTCBTC"]
    assert stats["paperAvgPnL"] == 0.025
    after()


def test_compStats():
    before()
    SU = StatsUpdate()
    statDict = SU.compStats(isTest=["testStrat1", "testStrat2"])
    assert len(list(statDict)) == 3
    totDict = statDict["total"]
    assert totDict["numberOpen"] == 2
    assert totDict["initialCapital"] == 20
    assert totDict["liquidCurrent"] == 18
    assert totDict["paperCurrent"] == 22
    assert totDict["percentAllocated"] == 18
    after()


if __name__ == "__main__":
    test_indivStats()
    test_compStats()
