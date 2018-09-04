from Pipeline.main.Deploy.Build import Build
from Pipeline.main.Deploy.Clean import Clean
from Pipeline.main.Deploy.Schedule import Schedule
from argparse import ArgumentParser


class Run:

    def __init__(self, stratParams):
        parser = ArgumentParser()
        parser.add_argument('--clean', default=False)
        parser.add_argument('--build', default=False)
        parser.add_argument('--run', default=True)
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