from Pipeline.main.Deploy.Build import Build
from Pipeline.main.Deploy.Clean import Clean
from Pipeline.main.Deploy.Schedule import Schedule
from argparse import ArgumentParser


class Run:

    def __init__(self, stratParams):
        parser = ArgumentParser()
        parser.add_argument('--clean', action='store_true', default=False)
        parser.add_argument('--build', action='store_true', default=False)
        parser.add_argument('--run', action='store_true', default=False)
        args = parser.parse_args()
        if args.build:
            Build(
                stratName=stratParams['stratName'],
                initialCapital=stratParams['initialCapital'], positionSizeParams=stratParams['positionSizeParams'],
                assetSelectionParams=stratParams['assetSelectionParams'], enterParams=stratParams['enterParams'],
                exitParams=stratParams['exitParams'],
                schedule=stratParams['schedule']
            )
        elif args.clean:
            Clean(stratName=stratParams['stratName'])
        if args.run:
            Schedule(strat=stratParams['stratName'], periodDict=stratParams['schedule']).run()
