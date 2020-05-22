import json

import pytest
import webtest
from simple_mailer.config import settings
from simple_mailer.http import Location
from simple_mailer.tests.fixtures.smtpd import SMTPServerFixture
from simple_mailer.tests.helpers import with_environ_var


def test_root_path_has_link_to_mailer(test_http_client):
    response = test_http_client.get("/")
    assert response.status_code == 200
    data = json.loads(response.body.decode("utf8"))
    assert data["mailer"] == settings.MAILER_PATH


def test_post_urlencode_mail_app(smtpd: SMTPServerFixture, test_http_client):
    response = test_http_client.post(
        "/mail", {"email": "me@example.com", "subscribe_me": True}
    )
    assert response.status_code == 200
    assert smtpd.sent_mail


def test_post_json_mail_app(smtpd: SMTPServerFixture, test_http_client):
    response = test_http_client.post_json(
        "/mail", {"email": "me@example.com", "subscribe_me": True}
    )
    assert response.status_code == 200
    assert smtpd.sent_mail
    body = smtpd.sent_mail[0].body.decode("utf8")
    assert "timestamp_utc" in body


@with_environ_var("REDIRECT_URL", "{{ ORIGIN }}")
def test_post_with_referer(smtpd: SMTPServerFixture, test_http_client):
    response = test_http_client.post_json(
        "/mail", {"email": "me@example.com", "subscribe_me": True},
        headers={'ORIGIN': 'http://www.example.org/thank-you'}
    )
    assert response.status_code == 302
    assert response.headers["Location"] == "http://www.example.org/thank-you"


@with_environ_var("REDIRECT_URL", "{{ REFERER }}")
def test_post_with_referer(smtpd: SMTPServerFixture, test_http_client):
    response = test_http_client.post_json(
        "/mail", {"email": "me@example.com", "subscribe_me": True},
        headers={'REFERER': 'http://www.example.org/thank-you'}
    )
    assert response.status_code == 302
    assert response.headers["Location"] == "http://www.example.org/thank-you"


def test_post_empty_payload_is_denied(test_http_client):
    try:
        test_http_client.post_json("/mail", {})
    except webtest.app.AppError as err:
        assert "400 Bad Request" in err.args[0]


def test_location_url():
    loc = Location("www.example.com", "/bar/foo")
    assert loc.https_url == "https://www.example.com/bar/foo"


@with_environ_var("REDIRECT_URL", "https://www.example.org/target")
def test_if_redirect_url_set_response_is_302(test_http_client):
    response = test_http_client.post_json(
        "/mail", {"email": "me@example.com", "subscribe_me": True}
    )
    assert response.status_code == 302
    assert response.headers["Location"] == "https://www.example.org/target"


def test_debug_not_available_without_env_var(test_http_client):
    with pytest.raises(webtest.app.AppError):
        test_http_client.get("/debug")


@with_environ_var("ENABLE_DEBUG", "true")
def test_debug_available_with_env_var(test_http_client):
    root_data = json.loads(test_http_client.get("/").body)
    debug_path = root_data["debug"]
    assert settings.DEBUG_PATH == debug_path
    response = test_http_client.get(debug_path)
    assert response.status_code == 200
    debug_data = json.loads(response.body)
    assert "version" in debug_data
    assert "environment_variables" in debug_data
    vars = debug_data["environment_variables"]
    assert len(vars) == len(type(settings).get_defaults())


@with_environ_var("ENABLE_DEBUG", "true")
def test_debug_can_test_smtpd_connection(test_http_client):
    response = test_http_client.get(settings.DEBUG_PATH)
    debug_data = json.loads(response.body)
    assert "smtp_connection" in debug_data
    assert debug_data["smtp_connection"] == {"status": "OK"}
