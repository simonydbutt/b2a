from Pipeline.main.Monitor.MarketDetails import MarketDetails
from Pipeline.main.Monitor.StatsUpdate import StatsUpdate
from email.message import EmailMessage
from datetime import datetime
import smtplib
import Settings


class EmailUtil:

    def __init__(self, strat=None, isTick=False):
        self.strat = strat
        self.isTick = isTick

    def _sendEmail(self, subject, content):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(
            user=Settings.EMAIL['USER'],
            password=Settings.EMAIL['PASSWORD']
        )
        msg = EmailMessage()
        msg['From'] = Settings.EMAIL['USER']
        msg['To'] = Settings.EMAIL['SEND_USER']
        msg['Subject'] = subject
        msg.set_content(content)
        server.send_message(msg=msg, from_addr=Settings.EMAIL['USER'], to_addrs=Settings.EMAIL['SEND_USER'])

    def errorExit(self, file, funct, message):
        self._sendEmail(
            subject='b2a Code Error',
            content='File:\t\t\t  %s\n'
                    'Function:\t     %s\n'
                    'Error message:\t%s' %
                    (file, funct, message)
        )

    def statsMessage(self):
        stats = StatsUpdate().compStats()[self.strat]
        msg = '-------------------------  %s -------------------------\n\n' \
              'Initial Capital: %s\nLiquid Current: %s\n' \
              'Paper Current: %s\nPaper PnL: %s%%\n' \
              'Percent Allocated: %s%%\nTrades Open: %s\n' \
              'Number Transactions: %s\nPaper Avg PnL: %s\n' % \
              (self.strat, stats['initialCapital'], stats['liquidCurrent'], stats['paperCurrent'],
               stats['paperPnL'], 100*stats['percentAllocated'], stats['numberOpen'],
               stats['numberTransactions'], stats['paperAvgPnL'])
        if len(stats['openList']) != 0:
            msg += 'Open Positions: %s' % '  '.join(stats['openList'])
        if self.isTick:
            msg += '\n\n-------------------------  Market Details  -------------------------\n\n'
            tickDict = MarketDetails().multiTicks((100, 1000))
            msg += 'Tick Data\n'
            for i in tickDict.keys():
                msg += '- %s Coins\n1h:  %s\n24h:  %s\n1w:  %s\n' % \
                       (i, tickDict[i]['short'], tickDict[i]['mid'], tickDict[i]['long'])
        self._sendEmail(subject='b2a Performance Stats: %s' % datetime.today().strftime('%Y-%m-%d %H:%M:%S'), content=msg)
