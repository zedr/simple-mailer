from webtest import TestApp

from simple_mailer.web import get_application


def test_post_mail_app(smtpd):
    app = TestApp(get_application())
    response = app.post(
        "/mail", {"email": "me@example.com", "subscribe_me": True}
    )
    assert response.status_code == 200
