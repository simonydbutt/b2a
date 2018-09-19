from Pipeline.main.Deploy.Run import Run
import logging


stratParams = {
    'stratName': 'OBD_PR',
    'initialCapital': 1,
    'positionSizeParams': {
        'name': 'Basic',
        'percent': 0.075
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
        'enterPercent': 1.1
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
        'exit': {'minute': '0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55'},
        'email': {
            'hour': '0, 5, 10, 15, 20',
            'minute': '16'
        }
    }
}


logging.basicConfig(level=logging.INFO)
Run(stratParams=stratParams)
