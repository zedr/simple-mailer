from typing import Dict, Any

from simple_mailer.config import settings
from simple_mailer.dispatcher import Dispatcher
from simple_mailer.exceptions import BaseSimpleMailerException

try:
    import pkg_resources
except ImportError:
    pkg_resources = None  # type: ignore


def get_version() -> str:
    """Get the version designation for this software distribution"""
    if pkg_resources:
        return pkg_resources.get_distribution("simple_mailer").version
    else:
        return "unknown"


def get_env_variables() -> Dict[str, Any]:
    """Get all the related environment variables and their values"""
    keys = settings.get_defaults().keys()
    return {key: settings[key] for key in keys}


def get_smtp_connection() -> Dict[str, str]:
    """Get information about the smtpd connection"""
    try:
        Dispatcher().get_server().connect().disconnect()
    except (BaseSimpleMailerException, OSError) as exc:
        return {"status": "error", "reason": f"{exc}"}
    else:
        return {"status": "OK"}
