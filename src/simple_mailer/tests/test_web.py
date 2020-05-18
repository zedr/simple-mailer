import json

import webtest
from simple_mailer.config import settings
from simple_mailer.http import Location
from simple_mailer.tests.fixtures.smtpd import SMTPServerFixture
from simple_mailer.tests.helpers import with_environ_var
from simple_mailer.web import get_application
from webtest import TestApp


def test_root_path_has_link_to_mailer():
    app = TestApp(get_application())
    response = app.get("/")
    assert response.status_code == 200
    data = json.loads(response.body.decode("utf8"))
    assert data["mailer"] == settings.MAILER_PATH


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
    body = smtpd.sent_mail[0].body.decode("utf8")
    assert "timestamp_utc" in body


def test_post_empty_payload_is_denied():
    app = TestApp(get_application())
    try:
        app.post_json("/mail", {})
    except webtest.app.AppError as err:
        assert "400 Bad Request" in err.args[0]


def test_location_url():
    loc = Location("www.example.com", "/bar/foo")
    assert loc.https_url == "https://www.example.com/bar/foo"


@with_environ_var("REDIRECT_URL", "https://www.example.org/target")
def test_if_redirect_url_set_response_is_302():
    app = TestApp(get_application())
    response = app.post_json(
        "/mail", {"email": "me@example.com", "subscribe_me": True}
    )
    assert response.status_code == 302
    assert response.headers["Location"] == "https://www.example.org/target"
