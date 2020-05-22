import re
from typing import Dict, Any

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
