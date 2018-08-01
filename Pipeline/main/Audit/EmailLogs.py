from Pipeline.main.Audit.DailyCapital import DailyCapital
from Pipeline.main.Audit.StratPerformance import StratPerformance
import datetime
import time
import Settings
import smtplib
from email.message import EmailMessage


class EmailLogs:

    def __init__(self):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(Settings.EMAIL_USER, Settings.EMAIL_PASSWORD)
        msg = EmailMessage()
        msg['Subject'] = 'B2B Performance Sandbox - %s' % datetime.datetime.fromtimestamp(round(time.time())).isoformat()
        msg['From'] = Settings.EMAIL_USER
        msg['To'] = Settings.EMAIL_SEND_USER
        msg.set_content(self.capitalMessage() + self.performanceMessage())
        self.server.send_message(msg=msg, from_addr=Settings.EMAIL_USER, to_addrs=Settings.EMAIL_SEND_USER)
        self.performanceMessage()

    def capitalMessage(self):
        dC = DailyCapital().run()
        return '-------------------------------  General  -------------------------------\n\n' \
               'Date:\t\t\t\t%s\nReal Capital:\t\t    $%s\nPaper Capital:\t\t   $%s\n' \
               'Percent Allocated:\t %s\nDaily Performance:\t%s\nTotal Performance:\t %s\n' \
               'Num. Open Trades:      %s\n\n\n' % (dC['Date'], dC['RealCapital'], dC['PaperCapital'],
                                                  dC['percentAllocated'], dC['dailyPerformance'],
                                                  dC['runningPerformance'], dC['numOpenTrades'])

    def performanceMessage(self):
        sD = StratPerformance().run()
        perfMessage = '------------------------------  Strategies  ------------------------------\n\n'
        for strat in sD.keys():
            stats = sD[strat]
            perfMessage += 'Strategy Name:  \t%s\n' \
                           'Num. Trades:\t\t %s\n' \
                           'PnL:\t\t\t      %s%%\n' \
                           'Win/Loss Ratio:\t\t%s\n' \
                           'Daily PnL:\t\t   %s\n' \
                           'Sharpe Ratio:\t\t %s\n' \
                           'Current Positions:\n%s\n\n' % (strat, stats['numTrades'], stats['percentPnL'],
                                                       stats['winLoss'], stats['changePnL'], stats['sharpeRatio'],
                                                       [trade['asset'] for trade in stats['currentTrades']])
        return perfMessage
