import random
import string

from webtest import TestApp

from simple_mailer import constants
from simple_mailer.web import get_application




def test_recaptcha_v3(smtpd, captcha_server, mocked_https_client):
    app = TestApp(get_application())
    recaptcha_response = ''.join(
        random.choice(string.ascii_letters) for idx in range(40)
    )
    response = app.post(
        "/mail",
        {
            "email": "me@example.com",
            "subscribe_me": True,
            constants.CaptchaResponseKeys.RECAPTCHA_V3: recaptcha_response
        }
    )
    assert response.status_code == 200
    assert smtpd.sent_mail
