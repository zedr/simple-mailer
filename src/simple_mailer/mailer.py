import smtplib
from email.message import EmailMessage


class NotConnectedError(Exception): pass


class Mailer:
    def __init__(self, host='localhost', port=465, use_tls=True):
        self.host = host
        self.port = port
        self.use_tls = use_tls
        self._conn = None
    
    def connect(self):
        if self.host and self.port > 0:
            self._conn = smtplib.SMTP(self.host, self.port)
            if self.use_tls:
                self._conn.starttls()
        else:
            raise NotConnectedError(
                f'Cannot connect to: {self.host}:{self.port}'
            )
    
    def login(self, userid, passwd):
        if self._conn is None:
            raise NotConnectedError('Not connected. Please connect first.')
        else:
            self._conn.login(userid, passwd)

    def send_message(self, from_='', to='', subject='', body=''):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = from_
        msg['To'] = to
        msg.set_content(body)
        self._conn.send_message(msg)

    def disconnect(self):
        self._conn.close()
