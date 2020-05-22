import json

from bottle import request, response, default_app, AppStack, get, post, run
from simple_mailer import checks
from simple_mailer import exceptions
from simple_mailer.config import settings
from simple_mailer.dispatcher import Dispatcher
from simple_mailer.utils import cloak, get_logger

log = get_logger(__name__)


@post(settings.MAILER_PATH)
def mail() -> str:
    """A resource that can send mail"""
    log.info(f"Got a new submission from client with IP {request.remote_addr}")
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


def run_application() -> None:
    run(host="localhost", port=8080)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", default="localhost", required=False, dest="host"
    )
    parser.add_argument(
        "--post", default=8080, type=int, required=False, dest="port"
    )
    parsed = parser.parse_args()
    run(host=parsed.host, port=parsed.port)


if __name__ == "__main__":
    main()
