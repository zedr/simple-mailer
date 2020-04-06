import smtplib
from dataclasses import dataclass
from email.message import EmailMessage
from typing import Optional


class NotConnectedError(Exception):
    """Not connected to the intended mail server"""


@dataclass
class Mailer:
    """An simple email client

    Attributes:
        host: the hostname of the server
        port: the port of the server
        use_tls: securely connect using TLS
    """

    host: str
    port: int = 465
    use_tls: bool = True
    _conn: smtplib.SMTP = Optional[None]

    def connect(self) -> None:
        """Connect to the remote server"""
        if self.host and self.port > 0:
            self._conn = smtplib.SMTP(host=self.host, port=self.port)
            if self.use_tls:
                self._conn.starttls()
        else:
            raise NotConnectedError(
                f"Cannot connect to: {self.host}:{self.port}"
            )

    def login(self, userid: str, passwd: str) -> None:
        """Login to the remote server

        Parameters:
            userid: the user id of the client
            passwd: the password of the client
        """
        if self._conn is None:
            raise NotConnectedError("Not connected. Please connect first.")
        else:
            self._conn.login(userid, passwd)

    def send_message(self, from_="", to="", subject="", body="") -> None:
        """Send an email message

        Parameters:
            from_: the sender email address
            to: the recipient email address
            subject: the subject of the email
            body: the body of the message
        """
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = from_
        msg["To"] = to
        msg.set_content(body)
        self._conn.send_message(msg)

    def disconnect(self) -> None:
        """Disconnect from the remote server"""
        self._conn.close()
