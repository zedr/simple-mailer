from simple_mailer.dispatcher import Dispatcher
from simple_mailer.tests.helpers import with_environ_var


def test_dispatcher_sends_email(smtpd, urlencoded_post_request):
    Dispatcher(data={"email": "me@example.com"}).dispatch()
    assert smtpd.sent_mail


def test_dispatcher_sends_text_templated_email(smtpd, urlencoded_post_request):
    Dispatcher(data={"email": "you@example.net", "msg": "hello!"}).dispatch()
    assert len(smtpd.sent_mail) == 1
    body = smtpd.sent_mail[0].body.decode("utf8")
    assert "Form submission" in body
    assert "msg: hello!" in body
    assert "timestamp_utc" in body


@with_environ_var("FIELDS_EXCLUDED", "subscribe_me")
def test_dispatcher_filter_unwanted_fields(smtpd, urlencoded_post_request):
    Dispatcher().parse_request(urlencoded_post_request).dispatch()
    assert len(smtpd.sent_mail) == 1
    body = smtpd.sent_mail[0].body.decode("utf8")
    assert "subscribe_me" not in body


@with_environ_var("FIELDS_INCLUDED", "subscribe_me")
def test_dispatcher_filter_wanted_fields(smtpd, urlencoded_post_request):
    Dispatcher().parse_request(urlencoded_post_request).dispatch()
    assert len(smtpd.sent_mail) == 1
    body = smtpd.sent_mail[0].body.decode("utf8")
    assert "email" not in body


@with_environ_var(
    "MAIL_SUBJECT", "IP {{metadata.client_ip}} sent a message: {{data.msg}}"
)
def test_mail_subject_can_be_defined_using_template_tags(smtpd):
    """The subject of the test mail can be configured using an env var"""
    dis = Dispatcher(data={"msg": "hello"}, metadata={"client_ip": "4.4.4.4"})
    dis.dispatch()
    body = smtpd.sent_mail[0].body.decode("utf8")
    assert "IP 4.4.4.4 sent a message: hello" in body
