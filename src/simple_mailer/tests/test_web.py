import os

from webtest import TestApp

from simple_mailer.web import get_application


def _set_test_environ(smtpd):
    os.environ.setdefault("SMTP_PORT", str(smtpd.port))
    os.environ.setdefault("USE_TLS", "false")
    os.environ.setdefault("FROM_ADDRESS", "me@example.com")
    os.environ.setdefault("TO_ADDRESS", "you@example.com")


def test_post_mail_app(smtpd):
    _set_test_environ(smtpd)
    app = TestApp(get_application())
    response = app.post("/mail", {})
    assert response.status_code == 200
