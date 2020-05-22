import json

from bottle import request, response, default_app, AppStack, get, post, run
from simple_mailer import checks
from simple_mailer import exceptions
from simple_mailer.config import settings
from simple_mailer.dispatcher import Dispatcher
from simple_mailer.utils import cloak


@post(settings.MAILER_PATH)
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
        redirect_url = settings.REDIRECT_URL
        if redirect_url:
            response.status = 302
            response.headers["Location"] = redirect_url
        else:
            response.status = 200
        return "OK"


@get(settings.DEBUG_PATH)
def debug() -> str:
    ns = {}
    if settings.ENABLE_DEBUG:
        ns.update(
            {
                "version": checks.get_version(),
                "environment_variables": cloak(checks.get_env_variables()),
                "smtp_connection": checks.get_smtp_connection(),
            }
        )
    else:
        response.status = 404
        ns["errors"] = "Debug not enabled"
    return json.dumps(ns)


@get("/")
def root() -> str:
    """The root resource"""
    ns = {"mailer": settings.MAILER_PATH}
    if settings.ENABLE_DEBUG:
        ns["debug"] = settings.DEBUG_PATH
    return json.dumps(ns)


def get_application() -> AppStack:
    """Get the default Bottle application"""
    return default_app()


def run_application():
    run(host="localhost", port=8080)
