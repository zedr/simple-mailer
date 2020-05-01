import os

from webtest import TestApp
from simple_mailer import constants
from simple_mailer.web import get_application


_recaptcha_response = ''


def test_recaptcha_v3(smtpd, captcha_server):
    app = TestApp(get_application())
    response = app.post(
        "/mail",
        {
            "email": "me@example.com",
            "subscribe_me": True,
            constants.CaptchaResponseKeys.RECAPTCHA_V3: _recaptcha_response
        }
    )
    assert response.status_code == 200
    assert smtpd.sent_mail
    assert False
