from urllib.parse import parse_qs

import bottle

from simple_mailer.config import Config
from simple_mailer.dispatcher import Dispatcher


@bottle.post(Config().MAILER_PATH)
def mail():
    body = bottle.request.body.read().decode("utf8")
    content_type = bottle.request.environ["CONTENT_TYPE"]
    if content_type == "application/x-www-form-urlencoded":
        data = parse_qs(body)
    else:
        return bottle.Response(status=406, body="Not acceptable")

    Dispatcher.dispatch(data)
    return "OK"


def get_application():
    return bottle.default_app()
