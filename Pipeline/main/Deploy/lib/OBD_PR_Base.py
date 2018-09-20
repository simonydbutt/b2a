from Pipeline.main.Deploy.Run import Run
import logging


stratParams = {
    'stratName': 'OBD_PR_BASE',
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
        'name': 'OrderBookDepth',
        'period': 900,
        'bookDepth': 50,
        'numTrades': 1000,
        'diffVals': [5, 10, 20],
        'enterPercent': 1.075
    },
    'exitParams': {
        'name': 'ProfitRun',
        'granularity': 900,
        'maPeriods': 90,
        'stdDict': {'up': 0.25, 'down': 1.5},
        'closePeriods': 50
    },
    'schedule': {
        'enter': {
            'minute': '3, 18, 33, 48',
        },
        'exit': {'minute': '2, 7, 12, 17, 22, 27, 32, 37, 42, 47, 52, 57'},
        'email': {
            'hour': '0, 5, 10, 15, 20',
            'minute': '16'
        }
    }
}


logging.basicConfig(level=logging.INFO)
Run(stratParams=stratParams)
