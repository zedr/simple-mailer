from simple_mailer.dispatcher import Dispatcher


def test_dispatcher_sends_email(smtpd, urlencoded_post_request):
    Dispatcher(data={"email": "me@example.com"}).dispatch()
    assert smtpd.sent_mail


def test_dispatcher_sends_text_templated_email(smtpd, urlencoded_post_request):
    Dispatcher(data={"email": "you@example.net"}).dispatch()
    assert len(smtpd.sent_mail) == 1
    assert smtpd.sent_mail
