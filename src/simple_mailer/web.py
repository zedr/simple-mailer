import json

from bottle import request, response, default_app, AppStack, get, post, run
from simple_mailer import exceptions
from simple_mailer.config import Config
from simple_mailer.dispatcher import Dispatcher


@post(Config().MAILER_PATH)
def mail() -> str:
    """A resource that can send mail"""
    try:
        Dispatcher().parse_request(request).dispatch()
    except exceptions.ContentTypeUnsupported as exc:
        response.status = 400
        return str(exc)
    except exceptions.SubmittedDataInvalid as exc:
        response.status = 400
        return str(exc)
    except exceptions.BaseSimpleMailerException as exc:
        response.status = 503
        return str(exc)
    else:
        redirect_url = Config().REDIRECT_URL
        if redirect_url:
            response.status = 302
            response.headers["Location"] = redirect_url
        else:
            response.status = 200
        return "OK"


@get("/")
def root() -> str:
    """The root resource"""
    return json.dumps({"mailer": Config().MAILER_PATH})


def get_application() -> AppStack:
    """Get the default Bottle application"""
    return default_app()


def run_application():
    run(host="localhost", port=8080)
