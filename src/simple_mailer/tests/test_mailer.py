import socket
import asyncore

import pytest

from simple_mailer.mailer import Mailer
from simple_mailer.tests.fixtures import smtpd


def get_free_port():
    s = socket.socket()
    s.bind(('', 0))
    return s.getsockname()[1]


def test_mailer_can_send_message(smtpd):
    mailer = Mailer(port=smtpd.port, use_tls=False)
    mailer.connect()
    mailer.login('userid', 'passwd')
    mailer.send_message(
        from_='me@example.com', 
        to='you@example.com',
        subject='test',
        body='Hello!'
    )
