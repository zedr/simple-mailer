import json
from urllib.parse import parse_qs

from bottle import request, response, default_app, AppStack, post
from simple_mailer.config import Config
from simple_mailer.dispatcher import Dispatcher


@post(Config().MAILER_PATH)
def mail() -> str:
    """A resource that can send mail"""
    body = request.body.read().decode("utf8")
    content_type = request.environ["CONTENT_TYPE"]
    if content_type == "application/x-www-form-urlencoded":
        data = parse_qs(body)
    else:
        data = json.loads(body)

    response.status = 200
    Dispatcher.dispatch(data)
    return "OK"


def get_application() -> AppStack:
    """Get the default Bottle application"""
    return default_app()
