from Pipeline.main.Monitor.MarketDetails import MarketDetails
from bs4 import BeautifulSoup
import Settings
import logging

# *TODO speed up!!!


def test_MarketTick():
    with open(
        "%s/Pipeline/tests/Monitor/MarketTickData.txt" % Settings.BASE_PATH, "r"
    ) as MTData:
        page = BeautifulSoup(MTData, "html.parser")
    assert MarketDetails().getTick(noCoins=1000, page=page)["short"] == -409
    assert MarketDetails().getTick(noCoins=100, page=page)["mid"] == -60


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    test_MarketTick()
