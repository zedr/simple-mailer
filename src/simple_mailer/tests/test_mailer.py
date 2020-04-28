from simple_mailer.mailer import Mailer


def test_mailer_can_send_message(smtpd):
    mailer = Mailer(port=smtpd.port, use_tls=False)
    mailer.connect()
    mailer.send_message(
        from_="me@example.com",
        to="you@example.com",
        subject="test",
        body="Hello!",
    )
    mailer.disconnect()
    assert smtpd.sent_mail
