from Pipeline.main.Deploy.Clean import Clean
from Pipeline.main.Deploy.Build import Build
from pymongo import MongoClient
import Settings
import shutil
import yaml
import os


path = "%s/Pipeline/resources/testClean" % Settings.BASE_PATH
client = MongoClient("localhost", 27017)
currentCol = client["testClean"]["currentPositions"]
transCol = client["testClean"]["transactionLogs"]


def before():
    after()
    Build(
        stratName="testClean",
        initialCapital=10,
        positionSizeParams={"name": "Basic", "percent": 0.05},
        assetSelectionParams={
            "name": "all",
            "exchangeList": ["Binance"],
            "baseAsset": "BTC",
        },
        enterParams={
            "name": "CheapVol",
            "granularity": 43200,
            "periodsVolLong": 100,
            "periodsVolShort": 5,
            "periodsMA": 100,
            "volCoef": 1.5,
            "bolStd": 2,
        },
        exitParams={
            "name": "ProfitRun",
            "granularity": 7200,
            "periodsVolLong": 50,
            "periodsVolShort": 5,
            "periodsMA": 50,
            "volCoef": 1,
            "bolStd": 2,
        },
        schedule={},
        isLive=False,
    )


def after():
    if os.path.exists(path):
        shutil.rmtree(path)


def test_cleanStrat():
    before()
    Clean(stratName="testClean").cleanStrat()
    assert not os.path.exists(path)
    assert "testClean" not in client.database_names()
    after()


def test_resetStrat():
    before()
    with open("%s/capital.yml" % path) as capFile:
        cap = yaml.load(capFile)
        cap["liquidCurrent"] = 0
    with open("%s/capital.yml" % path, "w") as capFile:
        yaml.dump(data=cap, stream=capFile)
    currentCol.insert_one({"a": 1})
    transCol.insert_many([{"a": 1, "b": 2}])
    Clean(stratName="testClean").resetStrat()
    assert currentCol.count() == 0
    assert transCol.count() == 0
    with open("%s/capital.yml" % path, "r+") as capFile:
        cap = yaml.load(capFile)
    assert cap == {
        "initialCapital": 10,
        "liquidCurrent": 10,
        "paperCurrent": 10,
        "paperPnL": 0,
        "percentAllocated": 0,
    }
    after()


if __name__ == "__main__":
    test_cleanStrat()
    test_resetStrat()
