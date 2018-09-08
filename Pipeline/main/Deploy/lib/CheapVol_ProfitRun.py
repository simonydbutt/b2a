from Pipeline.main.Deploy.Run import Run
import logging


stratParams = {
    'stratName': 'CheapVol_ProfitRun',
    'db': 'sandbox',
    'initialCapital': 1,
    'positionSizeParams': {
        'name': 'Basic',
        'percent': 0.05
    },
    'assetSelectionParams': {
        'name': 'All',
        'exchangeList': ['Binance'],
        'baseAsset': 'BTC'
    },
    'enterParams': {
        'name': 'CheapVol',
        'granularity': 21600,
        'periodsVolLong': 50,
        'periodsVolShort': 5,
        'periodsMA': 30,
        'volCoef': 1.2,
        'bolStd': 2
    },
    'exitParams': {
        'name': 'ProfitRun',
        'granularity': 21600,
        'maPeriods': 90,
        'stdDict': {'up': 0.25, 'down': 1.5},
        'closePeriods': 1080

    },
    'loggingParams': {
        'console': logging.DEBUG,
        'file': logging.INFO
    },
    'schedule': {
        'enter': {
            'hour': '5, 11, 17, 23',
            'minute': '2'
        },  # 1 hour ahead
        'exit': {'minute': '10, 40'},
        'email': {
            'hour': '5, 13, 20',
            'minute': '50'
        }
    }
}


Run(stratParams=stratParams)
