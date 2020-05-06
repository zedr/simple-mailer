import json

from simple_mailer.config import Config
from simple_mailer.tests.fixtures.smtpd import SMTPServerFixture
from simple_mailer.web import get_application
from webtest import TestApp


def test_root_path_has_link_to_mailer():
    app = TestApp(get_application())
    response = app.get('/')
    assert response.status_code == 200
    data = json.loads(response.body.decode('utf8'))
    assert data['mailer'] == Config().MAILER_PATH


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
    body = smtpd.sent_mail[0].body.decode('utf8')
    assert 'timestamp_utc' in body


def test_post_empty_payload():
    app = TestApp(get_application())
    response = app.post_json('/mail', {})
    assert response.status_code == 400
