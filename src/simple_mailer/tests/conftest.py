import io
import json
import os

import bottle
import pytest
from simple_mailer.config import Config
from simple_mailer.tests.fixtures.smtpd import SMTPServerFixture


@pytest.fixture(scope="session")
def smtpd(request):
    fixture = SMTPServerFixture()
    os.environ.setdefault("SMTP_PORT", str(fixture.port))
    os.environ.setdefault("USE_TLS", "false")
    os.environ.setdefault("FROM_ADDRESS", "me@example.com")
    os.environ.setdefault("TO_ADDRESS", "you@example.com")
    request.addfinalizer(fixture.close)
    return fixture


@pytest.fixture(autouse=True)
def reset(smtpd):
    smtpd.sent_mail.clear()


@pytest.fixture(scope="module")
def urlencoded_post_request():
    config = Config()
    body_obj = io.BytesIO(b'email=me%40example.com&subscribe_me=True')
    fixture = bottle.Request(
        environ={
            "REQUEST_METHOD": "POST",
            "PATH_INFO": config.MAILER_PATH,
            "CONTENT_TYPE": "application/x-www-form-urlencoded",
            "CONTENT_LENGTH": 40,
            "bottle.request.body": body_obj,
        }
    )
    return fixture


@pytest.fixture(scope="module")
def json_post_request():
    config = Config()
    body_obj = io.BytesIO(json.dumps(
        {
            'email': 'me@example.org',
            'message': 'hello!'
        }
    ))
    fixture = bottle.Request(
        environ={
            "REQUEST_METHOD": "POST",
            "PATH_INFO": config.MAILER_PATH,
            "CONTENT_TYPE": "application/x-www-form-urlencoded",
            "CONTENT_LENGTH": 40,
            "bottle.request.body": body_obj,
        }
    )
    return fixture
