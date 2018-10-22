from Pipeline.main.Monitor.MarketDetails import MarketDetails
from Pipeline.main.Monitor.StatsUpdate import StatsUpdate
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from datetime import datetime
import pandas as pd
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
        currentDF = pd.DataFrame([
            ['Initial Capital', stats['initialCapital']],
            ['Liquid Current', stats['liquidCurrent']],
            ['Paper Current', stats['paperCurrent']],
            ['Paper PnL', stats['paperPnL']],
            ['Percent Allocated', 100*stats['percentAllocated']],
            ['Trades Open', stats['numberOpen']],
            ['Number Transactions', stats['numberTransactions']]
        ], columns=['Total Stats', self.strat])
        msg = '<html lang = "en"><body><h2> B2A Performance Stats: %s</h2>' \
              '<h3>Total Stats</h3>%s<br><h3><h3>Current Positions</h3>%s' \
              % (self.strat, currentDF.set_index(keys='Total Stats', drop=True).to_html(),
                 StatsUpdate().getCurrentStats(stratName=self.strat).set_index(keys='assetName', drop=True).to_html())
        if self.isTick:
            msg += '\n\n-------------------------  Market Details  -------------------------\n\n'
            tickDict = MarketDetails().multiTicks((100, 1000))
            msg += 'Tick Data\n'
            tickDF = pd.DataFrame([
                ['1h', tickDict['100']['short'], tickDict['1000']['short']],
                ['24h', tickDict['100']['mid'], tickDict['1000']['mid']],
                ['1w', tickDict['100']['long'], tickDict['1000']['long']],
            ], columns=['Period', '  100  ', '  1000  '])
            msg += '<h3>Market Tick Data</h3>%s' % tickDF.set_index('Period', drop=True).to_html()
        msg += '</body></html>'
        self._sendEmail(subject='b2a Performance Stats: %s' % datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                        content=msg, html=True)
