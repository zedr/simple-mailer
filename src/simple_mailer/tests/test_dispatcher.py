from simple_mailer.dispatcher import Dispatcher


def test_dispatcher_sends_email(smtpd, urlencoded_post_request):
    Dispatcher({"email": "me@example.com"}).dispatch()
    assert smtpd.sent_mail


def test_dispatcher_sends_text_templated_email(smtpd, urlencoded_post_request):
    Dispatcher({"email": "me@example.com"}).dispatch()
    assert smtpd.sent_mail
