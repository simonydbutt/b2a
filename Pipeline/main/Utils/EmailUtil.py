from Pipeline.main.Monitor.StatsUpdate import StatsUpdate
from email.message import EmailMessage
from datetime import datetime
import smtplib
import Settings


class EmailUtil:

    def __init__(self, db=None):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(
            user=Settings.EMAIL['USER'],
            password=Settings.EMAIL['PASSWORD']
        )
        self.db = db

    def _sendEmail(self, subject, content):
        msg = EmailMessage()
        msg['From'] = Settings.EMAIL['USER']
        msg['To'] = Settings.EMAIL['SEND_USER']
        msg['Subject'] = subject
        msg.set_content(content)
        self.server.send_message(msg=msg, from_addr=Settings.EMAIL['USER'], to_addrs=Settings.EMAIL['SEND_USER'])

    def errorExit(self, file, funct, message):
        self._sendEmail(
            subject='b2a Code Error',
            content='File:\t\t\t  %s\n'
                    'Function:\t     %s\n'
                    'Error message:\t%s' %
                    (file, funct, message)
        )

    def statsMessage(self):
        stats = StatsUpdate(dbPath='Pipeline/DB/%s' % self.db).compStats()
        tStats = stats['total']
        msg = '-------------------------  Portfolio -------------------------\n\n' \
              'Initial Capital: %s\nLiquid Current: %s\n' \
              'Paper Current: %s\nPaper PnL: %s%%\n' \
              'Percent Allocated: %s%%\nTrades Open: %s\n\n\n' \
              '------------------------  Strategies  -------------------------\n\n' \
              % (tStats['initialCapital'], tStats['liquidCurrent'], tStats['paperCurrent'],
                 tStats['paperPnL'], tStats['percentAllocated'], tStats['numberOpen'])
        for strat in [val for val in stats.keys() if val != 'total']:
            iStats = stats[strat]
            msg += 'Strategy: %s\n' \
                   '\tInitial Capital: %s\n\tLiquid Current: %s\n' \
                   '\tPaper Current: %s\n\tPaper PnL: %s%%\n' \
                   '\tPercent Allocated: %s%%\t\nTrades Open: %s\n' \
                   '\tNumber Transactions: %s\t\nPaper Avg PnL: %s\n' \
                   '\tOpen List: %s\n\n' % \
                   (strat, iStats['initialCapital'], iStats['liquidCurrent'], iStats['paperCurrent'],
                    iStats['paperPnL'], iStats['percentAllocated'], iStats['numberOpen'],
                    iStats['numberTransactions'], iStats['paperAvgPnL'], iStats['openList'])
        self._sendEmail(subject='b2a Performance Stats: %s' % datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                        content=msg)
