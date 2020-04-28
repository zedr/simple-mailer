from bottle import request, response, default_app, AppStack, post
from simple_mailer.config import Config
from simple_mailer.dispatcher import Dispatcher


@post(Config().MAILER_PATH)
def mail() -> str:
    """A resource that can send mail"""

    response.status = 200
    Dispatcher().parse_request(request).dispatch()
    return "OK"


def get_application() -> AppStack:
    """Get the default Bottle application"""
    return default_app()
