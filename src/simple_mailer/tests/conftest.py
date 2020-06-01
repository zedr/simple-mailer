import io
import json
import os

import bottle
import pytest
from simple_mailer.config import settings
from simple_mailer.tests.fixtures.smtpd import SMTPServerFixture
from simple_mailer.web import get_application
from webtest import TestApp


@pytest.fixture(scope="session")
def smtpd(request):
    fixture = SMTPServerFixture()
    os.environ.setdefault("SMTP_PORT", str(fixture.port))
    os.environ.setdefault("USE_TLS", "false")
    os.environ.setdefault("FROM_ADDRESS", "me@example.com")
    os.environ.setdefault("TO_ADDRESS", "you@example.com")
    request.addfinalizer(fixture.close)
    return fixture


@pytest.fixture
def test_http_client():
    return TestApp(get_application())


@pytest.fixture(autouse=True)
def reset_smtpd_storage(smtpd):
    smtpd.sent_mail.clear()


@pytest.fixture(scope="module")
def urlencoded_post_request():
    body_obj = io.BytesIO(b"email=me%40example.com&subscribe_me=True")
    fixture = bottle.Request(
        environ={
            "REQUEST_METHOD": "POST",
            "PATH_INFO": settings.MAILER_PATH,
            "CONTENT_TYPE": "application/x-www-form-urlencoded",
            "CONTENT_LENGTH": 40,
            "bottle.request.body": body_obj,
        }
    )
    return fixture


@pytest.fixture(scope="module")
def json_post_request():
    body_obj = io.BytesIO(
        json.dumps({"email": "me@example.org", "message": "hello!"})
    )
    fixture = bottle.Request(
        environ={
            "REQUEST_METHOD": "POST",
            "PATH_INFO": settings.MAILER_PATH,
            "CONTENT_TYPE": "application/json",
            "CONTENT_LENGTH": 40,
            "bottle.request.body": body_obj,
        }
    )
    return fixture


@pytest.fixture
def captcha_server(request):
    os.environ.setdefault("CAPTCHA", "recaptchav3")
    recaptcha_site_key = "fIGZeiSgiRJDMMexWJmwAsMHAuWjwbcUwKvsgOAj"
    os.environ.setdefault("RECAPTCHAV3_SITE_KEY", recaptcha_site_key)

    def fin():
        os.environ.pop("CAPTCHA", None)
        os.environ.pop("RECAPTCHAV3_SITE_KEY", None)

    request.addfinalizer(fin)
    return {"key": recaptcha_site_key}


@pytest.fixture
def mocked_https_client(request):
    import http.client

    requests = []

    class MockedHTTPResponse:
        status = 200

        def read(self):
            return json.dumps({"success": True})

    class MockedHTTPSConnection:
        def __init__(self, host):
            self.host = host

        def request(self, method, path, params, headers):
            requests.append(
                {
                    "method": method,
                    "path": path,
                    "params": params,
                    "headers": headers
                }
            )

        def getresponse(self):
            return MockedHTTPResponse()

    _HTTPSConnection = http.client.HTTPSConnection
    http.client.HTTPSConnection = MockedHTTPSConnection

    def fin():
        http.client.HTTPSConnection = _HTTPSConnection

    request.addfinalizer(fin)
    return requests
