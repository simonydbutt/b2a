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

    def __init__(self, stratName, initialCapital, positionSizeParams, enterParams, assetSelectionParams,
                 exitParams, schedule, isLive):
        logging.debug('Initialising Build(): %s' % stratName)
        self.compPath = '%s/Pipeline/resources/%s' % (Settings.BASE_PATH, stratName)
        logging.debug('compPath: %s' % self.compPath)
        if os.path.exists(self.compPath):
            print('Strat already exists. Print Y to overwrite')
            if input() == 'Y':
                logging.warning('Rewriting strategy')
                self.buildStrat(stratName=stratName, assetSelectionParams=assetSelectionParams,
                                positionSizeParams=positionSizeParams, enterParams=enterParams, exitParams=exitParams,
                                initialCapital=initialCapital, schedule=schedule, isLive=isLive)
            else:
                logging.warning('No action to be taken')
        else:
            self.buildStrat(stratName=stratName, assetSelectionParams=assetSelectionParams,
                            positionSizeParams=positionSizeParams, enterParams=enterParams, exitParams=exitParams,
                            initialCapital=initialCapital, schedule=schedule, isLive=isLive)

    def buildStrat(self, stratName, assetSelectionParams, positionSizeParams,
                   enterParams, exitParams, initialCapital, schedule, isLive):
        configDict = {
            'stratName': stratName, 'assetSelection': assetSelectionParams,
            'positionSize': positionSizeParams, 'enter': enterParams, 'exit': exitParams,
            'schedule': schedule, 'isLive': isLive
        }
        for path in ('%s/Pipeline/resources' % Settings.BASE_PATH, self.compPath):
            os.mkdir(path) if not os.path.isdir(path) else None
        with open('%s/config.yml' % self.compPath, 'w') as configFile:
            yaml.dump(configDict, configFile)
        with open('%s/capital.yml' % self.compPath, 'w') as capFile:
            yaml.dump({
                    'initialCapital': initialCapital, 'liquidCurrent': initialCapital,
                    'paperCurrent': initialCapital, 'paperPnL': 0,
                    'percentAllocated': 0
                }, capFile)
        logging.info('Build Complete')
