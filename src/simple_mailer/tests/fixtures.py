from smtpd import SMTPServer
from threading import Lock, Thread
import asyncore
import time

import pytest


class SMTPServerThread(Thread):
    def __init__(self):
        super().__init__()
        self.host_port = None
        self._processed_message = False

    def run(self):
        thread = self

        class _SMTPServer(SMTPServer):
            def process_message(self, *args, **kwargs):
                thread._processed_message = True

        self.smtp = _SMTPServer(('127.0.0.1', 0), None)
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
        '''SMTP server's listening address as a (host, port) tuple'''
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
        self._thread.close()
        self._thread.join(10)
        if self._thread.is_alive():
            raise RuntimeError('smtp server thread did not stop in 10 sec')


@pytest.fixture
def smtpd(request):
    fixture = SMTPServerFixture()
    request.addfinalizer(fixture.close)
    return fixture