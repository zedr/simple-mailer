import pytest
from simple_mailer.mailer import Mailer
from simple_mailer.exceptions import SmtpServerNotConfiguredError


def test_mailer_without_smtp_host_raises_error(smtpd):
    mailer = Mailer(port=smtpd.port, use_tls=False)
    with pytest.raises(SmtpServerNotConfiguredError):
        mailer.connect()


def test_mailer_can_send_message(smtpd):
    mailer = Mailer(host="localhost", port=smtpd.port, use_tls=False)
    mailer.connect()
    mailer.send_message(
        from_="me@example.com",
        to="you@example.com",
        subject="test",
        body="Hello!",
    )
    mailer.disconnect()
    assert smtpd.sent_mail
