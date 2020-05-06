import asyncore
import time
from smtpd import SMTPChannel, SMTPServer
from threading import Thread
from types import SimpleNamespace
from typing import List, Optional


class CustomSMTPChannel(SMTPChannel):
    def smtp_AUTH(self, arg):
        self.push("235 2.7.0 Authentication successful")


class SMTPServerThread(Thread):
    def __init__(self):
        super().__init__()
        self.host_port: Optional[int] = None
        self.sent_mail: list = []

    def run(self):
        server_thread = self

        class _SMTPServer(SMTPServer):
            channel_class = CustomSMTPChannel

            def process_message(
                self,
                _: tuple,
                sender: str,
                recipients: List[str],
                msg: bytes,
                *args,
                **kwargs,
            ):
                server_thread.sent_mail.append(
                    SimpleNamespace(
                        **{"from": sender, "to": recipients, "body": msg}
                    )
                )

        self.smtp = _SMTPServer(("localhost", 0), None)
        self.host_port = self.smtp.socket.getsockname()
        asyncore.loop(timeout=0.1)

    def close(self):
        self.smtp.close()


class SMTPServerFixture:
    def __init__(self):
        self._thread = SMTPServerThread()
        self._thread.start()

    @property
    def host_port(self):
        """SMTP server's listening address as a (host, port) tuple"""
        while self._thread.host_port is None:
            time.sleep(0.1)
        return self._thread.host_port

    @property
    def host(self):
        return self.host_port[0]

    @property
    def port(self):
        return self.host_port[1]

    def close(self):
        self._thread.sent_mail.clear()
        self._thread.close()
        self._thread.join(10)
        if self._thread.is_alive():
            raise RuntimeError("smtp server thread did not stop in 10 sec")

    @property
    def sent_mail(self) -> list:
        return self._thread.sent_mail
