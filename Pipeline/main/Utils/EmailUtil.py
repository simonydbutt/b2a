from Pipeline.main.Monitor.StatsUpdate import StatsUpdate
from email.message import EmailMessage
from datetime import datetime
import smtplib
import Settings


class EmailUtil:

    def __init__(self, db=None, strat=None):
        self.db = db
        self.strat = strat

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
        stats = StatsUpdate(dbPath='Pipeline/DB/%s' % self.db).compStats()[self.strat]
        msg = '-------------------------  %s -------------------------\n\n' \
              '\tInitial Capital: %s\n\tLiquid Current: %s\n' \
              '\tPaper Current: %s\n\tPaper PnL: %s%%\n' \
              '\tPercent Allocated: %s%%\t\nTrades Open: %s\n' \
              '\tNumber Transactions: %s\t\nPaper Avg PnL: %s\n' \
              '\tOpen List: %s\n\n' % \
              (self.strat, stats['initialCapital'], stats['liquidCurrent'], stats['paperCurrent'],
               stats['paperPnL'], 100*stats['percentAllocated'], stats['numberOpen'],
               stats['numberTransactions'], stats['paperAvgPnL'], stats['openList'])
        self._sendEmail(subject='b2a Performance Stats: %s' % datetime.today().strftime('%Y-%m-%d %H:%M:%S'), content=msg)
