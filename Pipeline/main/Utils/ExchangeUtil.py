class ExchangeUtil:

    def __init__(self):
        self.exchangeDict = {
            'Binance': {
                'interval': {
                    '60': '1m', '180': '3m', '300': '5m', '900': '15m',
                    '1800': '30m', '3600': '1h', '7200': '2h',
                    '14400': '4h', '21600': '6h', '28800': '8h',
                    '43200': '12h', '86400': '1d', '259200': '3d',
                    '604800': '1w'
                },
                'columns': ['milliTSOpen', 'open', 'high', 'low', 'close', 'volume',
                            'milliTSClose', 'quoteVol', 'numTrades', 'takerBaseVol',
                            'takerQuoteVol', 'id_'],
                'fees': 0.001
            },
            'Hadax': {
                'interval': {
                    '60': '1min', '300': '5min', '900': '15min',
                    '3600': '60min', '86400': '1day', '604800': '1week'
                },
                'columns': ['TS', 'open', 'close', 'low', 'high', 'amount', 'vol', 'count'],
                'fees': 0.002
            }
        }

    def candlestickInterval(self, period, exchange):
        return self.exchangeDict[exchange]['interval'][str(period)] if exchange in self.exchangeDict.keys() else -1

    def candlestickColumns(self, exchange):
        return self.exchangeDict[exchange]['columns']

    def fees(self, exchange):
        return self.exchangeDict[exchange]['fees']
