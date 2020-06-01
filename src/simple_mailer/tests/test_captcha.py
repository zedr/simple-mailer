import random
import string
import urllib.parse

from simple_mailer import captcha
from simple_mailer.dispatcher import Dispatcher
from simple_mailer.tests.helpers import with_environ_var
from simple_mailer.web import get_application
from webtest import TestApp


@with_environ_var("CAPTCHA_TYPE", "recaptchav3")
@with_environ_var("CAPTCHA_VERIFY_URL", "http://www.example.org/verify")
def test_captcha_interface(captcha_server, mocked_https_client):
    """Test the behaviour of the generic captcha object

    The HTTPS url is always forced.
    """
    client = captcha.CaptchaClient.from_environment()
    assert client.validate_data({client.key: "abc"}) is None
    assert client.location.https_url == "https://www.example.org/verify"
    params = urllib.parse.parse_qs(mocked_https_client[0]["params"])
    assert params["response"] == ["abc"]


def test_recaptcha_v3(smtpd, captcha_server, mocked_https_client):
    app = TestApp(get_application())
    recaptcha_response = "".join(
        random.choice(string.ascii_letters) for _ in range(40)
    )
    response = app.post(
        "/mail",
        {
            "email": "me@example.com",
            "subscribe_me": True,
            captcha.Recaptchav3Client.key: recaptcha_response,
        },
    )
    assert response.status_code == 200
    assert smtpd.sent_mail


@with_environ_var("FIELDS_INCLUDED", "delete_me")
@with_environ_var("CAPTCHA_TYPE", "recaptchav3")
def test_captcha_field_implictly_included():
    data = {
        "delete_me": "now",
        captcha.Recaptchav3Client.key: "abcdefgh1234",
    }
    assert captcha.Recaptchav3Client.key in data
    dispatcher = Dispatcher(data=data).process_data()
    assert captcha.Recaptchav3Client.key in dispatcher.data
