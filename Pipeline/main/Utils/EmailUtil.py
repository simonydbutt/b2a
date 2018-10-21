from Pipeline.main.Monitor.MarketDetails import MarketDetails
from Pipeline.main.Monitor.StatsUpdate import StatsUpdate
from Pipeline.main.Utils.Visualise import Visualise
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from datetime import datetime
import smtplib
import Settings
import os


class EmailUtil:

    def __init__(self, strat=None, isTick=False):
        self.strat = strat
        self.isTick = isTick

    def _sendEmail(self, subject, content, imgPath=None, html=False):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(
            user=Settings.EMAIL['USER'],
            password=Settings.EMAIL['PASSWORD']
        )
        msg = MIMEMultipart()
        msg['From'] = Settings.EMAIL['USER']
        msg['To'] = Settings.EMAIL['SEND_USER']
        msg['Subject'] = subject
        msg.attach(
            MIMEText(content, _subtype='plain') if not html
            else MIMEText(content, _subtype='html')
        )
        if imgPath:
            msg.attach(MIMEImage(open(imgPath, 'rb').read(), name=os.path.basename(imgPath)))
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
        msg = '<html lang = "en"><body><h2> B2A Performance Stats: %s</h2><br><table><tr><th>Initial Capital </th>' \
              '<td> %s</td></tr><tr><th>Liquid Current </th><td> %s</td></tr><tr><th>Paper Current </th><td> %s</td>' \
              '</tr><tr><th>Paper PnL </th><td> %s</td></tr><tr><th>Percent Allocated </th><td> %s</td></tr><tr>' \
              '<th>Trades Open </th><td> %s</td></tr><tr><th>Number Transactions </th><td> %s</td></tr><tr>' \
              '<th>Paper Avg PnL </th><td> %s</td></tr></table><br><h3>Current Positions</h3>' \
              % (self.strat, stats['initialCapital'], stats['liquidCurrent'], stats['paperCurrent'], stats['paperPnL'],
                 100*stats['percentAllocated'], stats['numberOpen'], stats['numberTransactions'], stats['paperAvgPnL'])
        msg += StatsUpdate().getCurrentStats(stratName=self.strat).to_html()
        msg += '</body></html>'
        if self.isTick:
            msg += '\n\n-------------------------  Market Details  -------------------------\n\n'
            tickDict = MarketDetails().multiTicks((100, 1000))
            msg += 'Tick Data\n'
            for i in tickDict.keys():
                msg += '- %s Coins\n1h:  %s\n24h:  %s\n1w:  %s\n' % \
                       (i, tickDict[i]['short'], tickDict[i]['mid'], tickDict[i]['long'])
        self._sendEmail(subject='b2a Performance Stats: %s' % datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                        content=msg, html=True)
