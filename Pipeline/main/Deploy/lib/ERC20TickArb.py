from Pipeline.main.Deploy.Run import Run
import logging
import urllib3

stratParams = {
    'stratName': 'ERC20TickArb',
    'isLive': False,
    'statArb': True,
    'initialCapital': 1,
    'positionSizeParams': {},
    'assetSelectionParams': {},
    'enterParams': {
        'enterVal': 15,
        'name': 'ERC20TickFade',
        'assetList': {
            'erc': [
                'BNB', 'VET', 'OMG', 'MKR', 'ZRX', 'ZIL', 'ICX', 'AE', 'NPXS', 'BTM', 'BAT', 'GNT', 'REP', 'HOT', 'SNT',
                'PPT', 'WTC', 'LINK', 'IOST', 'AION', 'ELF', 'BNT', 'DCN', 'FUN', 'QASH', 'MANA', 'NAS', 'DGD', 'CMT',
                'PAY', 'MCO', 'WAX', 'THETA', 'POWR', 'LOOM', 'LRC', 'DRGN', 'DAI', 'POLY', 'KNC', 'SUB', 'NEXO', 'KIN',
                'DENT', 'NOAH', 'NULS', 'ENG', 'OCN', 'ENJ', 'CVC'
            ],
            'non': [
                'XRP', 'BCH', 'EOS', 'XLM', 'LTC', 'ADA', 'XMR', 'KMD', 'DASH', 'TRX', 'NEO', 'XTZ', 'DOGE', 'BCN',
                'BTG', 'LSK', 'ONT', 'QTUM', 'DCR', 'NANO', 'SC', 'XVG', 'WAVES', 'ETP', 'STRAT', 'CNX', 'ARDR', 'WAN',
                'RDD', 'MITH', 'MONA', 'ARK', 'NXT', 'XZC', 'BTCP', 'SYS', 'NXS', 'FCT', 'NMC', 'SKY', 'RVN', 'NEBL',
                'BLOCK', 'PPC', 'XDN', 'UBQ', 'GO', 'BAY', 'POA', 'ICN'
            ],
        },
        'maxVolCoef': 0.95
    },
    'exitParams': {
        'maxPeriods': 4,
        'name': 'ERC20TickFade'
    },
    'schedule': {
        'enter': {
            'minute': '5, 20, 35, 50'
        },
        'exit': {'minute': '4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 55, 59'},
        'email': {
            'hour': '7, 12, 17, 22',
            'minute': '50'
        }
    }
}


urllib3.disable_warnings()
logging.basicConfig(level=logging.INFO)
Run(stratParams=stratParams)
