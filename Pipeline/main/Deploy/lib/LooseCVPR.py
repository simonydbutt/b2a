from Pipeline.main.Deploy.Run import Run
import logging


stratParams = {
    'stratName': 'LooseCVPR',
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
        'periodsVolLong': 50,
        'periodsVolShort': 5,
        'periodsMA': 50,
        'volCoef': 1.5,
        'bolStd': 1.5
    },
    'exitParams': {
        'name': 'ProfitRun',
        'granularity': 21600,
        'maPeriods': 50,
        'stdDict': {'up': 0.25, 'down': 1},
        'closePeriods': 500
    },
    'schedule': {
        'enter': {
            'hour': '5, 11, 17, 23',
            'minute': '6'
        },  # 1 hour ahead
        'exit': {'minute': '10, 40'},
        'email': {
            'hour': '5, 13, 20',
            'minute': '50'
        }
    }
}


logging.basicConfig(level=logging.INFO)
Run(stratParams=stratParams)
