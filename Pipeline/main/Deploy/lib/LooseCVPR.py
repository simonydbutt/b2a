from Pipeline.main.Deploy.Run import Run
import logging


stratParams = {
    'stratName': 'LooseCVPR',
    'db': 'sandbox',
    'initialCapital': 1,
    'positionSizeParams': {
        'name': 'Basic',
        'percent': 0.02
    },
    'assetSelectionParams': {
        'name': 'All',
        'exchangeList': ['Binance'],
        'baseAsset': 'BTC'
    },
    'enterParams': {
        'name': 'CheapVol',
        'granularity': 21600,
        'periodsVolLong': 100,
        'periodsVolShort': 5,
        'periodsMA': 100,
        'volCoef': 1,
        'bolStd': 1
    },
    'exitParams': {
        'name': 'ProfitRun',
        'granularity': 21600,
        'maPeriods': 50,
        'stdDict': {'up': 0.25, 'down': 1},
        'closePeriods': 1200
    },
    'loggingParams': {
        'console': logging.DEBUG,
        'file': logging.INFO
    },
    'schedule': {
        'enter': {
            'hour': '5, 19',
            'minute': '6'
        },  # 1 hour ahead
        'exit': {'minute': '10, 40'},
        'email': {
            'hour': '5, 13, 21',
            'minute': '50'
        }
    }
}


Run(stratParams=stratParams)
