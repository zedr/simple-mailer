from simple_mailer.dispatcher import Dispatcher


def test_dispatcher_reads_urlencoded_data(smtpd, urlencoded_post_request):
    dispatcher = Dispatcher()
    dispatcher.dispatch({"email": "me@example.com"})


def test_dispatcher_reads_json_data():
    pass
