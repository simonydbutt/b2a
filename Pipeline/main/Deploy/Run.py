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
                stratName=stratParams['stratName'], dbName=stratParams['db'],
                initialCapital=stratParams['initialCapital'], positionSizeParams=stratParams['positionSizeParams'],
                assetSelectionParams=stratParams['assetSelectionParams'], enterParams=stratParams['enterParams'],
                exitParams=stratParams['exitParams'], loggingParams=stratParams['loggingParams'],
                schedule=stratParams['schedule']
            )
        elif args.clean:
            Clean(db=stratParams['db'], stratName=stratParams['stratName'])
        if args.run:
            Schedule(db=stratParams['db'], strat=stratParams['stratName'], periodDict=stratParams['schedule']).run()
