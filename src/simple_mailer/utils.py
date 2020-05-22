import re
import logging
from typing import Dict, Any

from simple_mailer.config import settings

_sensitive_rxp = re.compile(r"^\w+(_SECRET|_PASSWD)$")


def cloak(ns: Dict[str, Any], stub="********") -> Dict:
    """Cloak sensitive variables to not reveal secrets"""
    cloaked_ns = {}
    for key, val in ns.items():
        if val and _sensitive_rxp.match(key):
            cloaked_ns[key] = stub
        else:
            cloaked_ns[key] = val
    return cloaked_ns


def get_logger(name, handler_cls=logging.StreamHandler) -> logging.Logger:
    """Get a named logger"""
    log = logging.getLogger(name)
    log.setLevel(settings.LOG_LEVEL)
    log.addHandler(handler_cls())
    return log
