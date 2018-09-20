from bokeh.plotting import figure
from bokeh.io import export_png
from pymongo import MongoClient
import pandas as pd
import Settings
import logging


class Visualise:

    def __init__(self):
        logging.debug('Initialising Visualise()')
        self.client = MongoClient('localhost', 27017)

    def plotTrades(self, stratName):
        logging.debug('Starting Visualise.plotTrades')

        transCol = self.client[stratName]['transactionLogs']
        currCol = self.client[stratName]['currentPositions']
        if transCol.count_documents() != 0 or currCol.count_documents != 0:
            p = figure(plot_width=800, plot_height=500)
            p.yaxis.axis_label = 'PnL (%)'
            p.xaxis.axis_label = 'Periods'
            if transCol.count_documents() != 0:
                dfT = pd.DataFrame(list(transCol.find({}, {'_id': 0, 'periods': 1, 'realPnL': 1})))
                dfT['realPnL'] *= 100
                p.circle(dfT['periods'], dfT['realPnL'], size=5, color='red')
            if currCol.count_documents():
                dfC = pd.DataFrame(list(currCol.find({}, {'_id': 0, 'periods': 1, 'openPrice': 1, 'currentPrice': 1})))
                dfC['realPnL'] = 100 * (dfC['currentPrice'] - dfC['openPrice']) / dfC['openPrice']
                p.cross(dfC['periods'], dfC['realPnL'], size=5, color='blue')
            export_png(p, filename='%s/Pipeline/resources/%s/pnLGraph.png' % (Settings.BASE_PATH, stratName))
        else:
            logging.info('Not enough trades for visualisation')


Visualise().plotTrades(stratName='OBD_PR')