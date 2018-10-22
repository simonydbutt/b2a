from Pipeline.main.Deploy.Build import Build
from Pipeline.main.Deploy.Clean import Clean
from Pipeline.main.Deploy.Schedule import Schedule
from argparse import ArgumentParser
import urllib3


class Run:
    def __init__(self, stratParams):
        parser = ArgumentParser()
        parser.add_argument("--clean", action="store_true", default=False)
        parser.add_argument("--build", action="store_true", default=False)
        parser.add_argument("--run", action="store_true", default=False)
        args = parser.parse_args()
        urllib3.disable_warnings()
        if args.build:
            Build(
                stratName=stratParams["stratName"],
                initialCapital=stratParams["initialCapital"],
                positionSizeParams=stratParams["positionSizeParams"],
                assetSelectionParams=stratParams["assetSelectionParams"],
                enterParams=stratParams["enterParams"],
                exitParams=stratParams["exitParams"],
                schedule=stratParams["schedule"],
                isLive=stratParams["isLive"],
                statArb=stratParams["statArb"]
                if "statArb" in stratParams.keys()
                else False,
            )
        elif args.clean:
            Clean(stratName=stratParams["stratName"]).resetStrat()
        if args.run:
            Schedule(
                strat=stratParams["stratName"], periodDict=stratParams["schedule"]
            ).run()
