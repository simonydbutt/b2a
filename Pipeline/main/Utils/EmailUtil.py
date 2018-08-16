from email.message import EmailMessage
import smtplib
import Settings


class EmailUtil:

    def __init__(self):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(
            user=Settings.EMAIL['USER'],
            password=Settings.EMAIL['PASSWORD']
        )

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
