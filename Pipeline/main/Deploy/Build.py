from tinydb import TinyDB
import Settings
import logging
import yaml
import os


class Build:

    """
        __Requirements__

        enterParams*
            - name
            - granularity

        exitParams*
            - name
            - granularity

        positionSizeParams*
            - name

        assetSelectionParams*
            - name
            - exchangeList
            - baseAsset

        * Indiv requirements are noted at top of class
    """

    def __init__(self, dbName, stratName, initialCapital, positionSizeParams, enterParams, assetSelectionParams,
                 exitParams, schedule, loggingParams={'console': logging.WARNING, 'file': logging.INFO}):
        self.compPath = '%s/Pipeline/DB/%s/%s' % (Settings.BASE_PATH, dbName, stratName)
        if os.path.exists(self.compPath):
            print('Strat already exists. Print Y to overwrite')
            if input() == 'Y':
                self.buildStrat(stratName=stratName, assetSelectionParams=assetSelectionParams, dbName=dbName,
                                positionSizeParams=positionSizeParams, enterParams=enterParams, exitParams=exitParams,
                                loggingParams=loggingParams, initialCapital=initialCapital, schedule=schedule)
        else:
            self.buildStrat(stratName=stratName, assetSelectionParams=assetSelectionParams, dbName=dbName,
                            positionSizeParams=positionSizeParams, enterParams=enterParams, exitParams=exitParams,
                            loggingParams=loggingParams, initialCapital=initialCapital, schedule=schedule)

    def buildStrat(self, stratName, assetSelectionParams, dbName, positionSizeParams,
                   enterParams, exitParams, loggingParams, initialCapital, schedule):
        configDict = {
            'stratName': stratName, 'assetSelection': assetSelectionParams,
            'positionSize': positionSizeParams, 'enter': enterParams, 'exit': exitParams,
            'logging': loggingParams, 'dbName': dbName, 'schedule': schedule
        }
        for path in ('%s/Pipeline/DB/%s' % (Settings.BASE_PATH, dbName), self.compPath, '%s/CodeLogs' % self.compPath):
            os.mkdir(path) if not os.path.isdir(path) else None
        with open('%s/config.yml' % self.compPath, 'w') as configFile:
            yaml.dump(configDict, configFile)
        with open('%s/capital.yml' % self.compPath, 'w') as capFile:
            yaml.dump(
                {
                    'initialCapital': initialCapital,
                    'liquidCurrent': initialCapital,
                    'paperCurrent': initialCapital,
                    'paperPnL': 0,
                    'percentAllocated': 0
                },
                capFile
            )
        TinyDB('%s/currentPositions.ujson' % self.compPath)
        TinyDB('%s/transactionLogs.ujson' % self.compPath)
