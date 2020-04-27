from simple_mailer.tests.fixtures.smtpd import SMTPServerFixture
from simple_mailer.web import get_application
from webtest import TestApp


def test_post_urlencode_mail_app(smtpd: SMTPServerFixture):
    app = TestApp(get_application())
    response = app.post(
        "/mail", {"email": "me@example.com", "subscribe_me": True}
    )
    assert response.status_code == 200
    assert smtpd.sent_mail


def test_post_json_mail_app(smtpd: SMTPServerFixture):
    app = TestApp(get_application())
    response = app.post_json(
        "/mail", {"email": "me@example.com", "subscribe_me": True}
    )
    assert response.status_code == 200
    assert smtpd.sent_mail
