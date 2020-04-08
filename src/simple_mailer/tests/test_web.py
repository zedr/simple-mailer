from webtest import TestApp

from simple_mailer.web import get_application
from simple_mailer.tests.fixtures.smtpd import SMTPServerFixture


def test_post_mail_app(smtpd: SMTPServerFixture):
    app = TestApp(get_application())
    response = app.post(
        "/mail", {"email": "me@example.com", "subscribe_me": True}
    )
    assert response.status_code == 200
    assert smtpd.sent_mail
