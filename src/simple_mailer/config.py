import logging
import os
from pathlib import Path
from typing import Optional, Any, Dict
from urllib.parse import urlparse

from bottle import request
from jinja2 import Template
from simple_mailer.exceptions import ConfigError
from simple_mailer.http import Location

_supported_log_level_names = ("DEBUG", "INFO", "WARN", "ERROR", "CRITICAL")


class BoolStr:
    """A factory class that can construct booleans from strings"""

    def __new__(cls, value, *args, **kwargs):
        if hasattr(value, "lower"):
            return bool(value.lower() == "true")
        else:
            return bool(value)


class TupleStr:
    sep = ","

    def __new__(cls, value, *args, **kwargs):
        if value and hasattr(value, "split"):
            return tuple(value.split(cls.sep))
        else:
            return tuple(value)


class _ConfigValueTypeChecker(type):
    """Check that the type definitions for the given class are supported"""

    supported_types = (int, float, str, bytes, bool, BoolStr, tuple, TupleStr)

    def __new__(cls, name, bases, ns):
        try:
            annotations: dict = ns["__annotations__"]
        except KeyError:
            pass
        else:
            for key, typ in annotations.items():
                if typ not in cls.supported_types:
                    raise TypeError(
                        f'Unsupported config variable type "{typ}" '
                        f'for key "{key}". '
                        f"Supported types are: {cls.supported_types}"
                    )

        return super().__new__(cls, name, bases, ns)


class _ConfigurationSettings:
    """A basic, lazily loaded configuration object."""

    class Defaults(metaclass=_ConfigValueTypeChecker):
        """Default values need to be specified for each configuration var.

        If not specified, the default type will be str.

        Only certain types are supported, e.g. str, float, bool, etc.
        See the metaclass for more information."""

        SMTP_HOST: str = "localhost"
        SMTP_PORT: int = 465
        SMTP_USERID: str = ""
        SMTP_PASSWD: str = ""
        TO_ADDRESS: str = ""
        FROM_ADDRESS: str = ""
        MAIL_SUBJECT: str = ""
        MAIL_TEMPLATE_PATH = (
                Path(__file__).parent / "templates" / "default.txt"
        )
        MAILER_PATH: str = "/mail"
        USE_TLS: BoolStr = BoolStr(True)
        CAPTCHA_TYPE: str = ""
        CAPTCHA_SECRET: str = ""
        CAPTCHA_VERIFY_URL: str = ""
        REDIRECT_URL: str = ""
        FIELDS_INCLUDED: TupleStr = TupleStr("")
        FIELDS_EXCLUDED: TupleStr = TupleStr("")
        ENABLE_DEBUG: BoolStr = BoolStr(False)
        DEBUG_PATH: str = "/debug"
        LOG_LEVEL: str = "WARN"

    def _get(self, name: str) -> Any:
        try:
            val = os.environ.get(name, getattr(self.Defaults, name))
        except AttributeError:
            raise ConfigError(f"Unsupported configuration parameter: {name}")
        else:
            typ = self.Defaults.__annotations__.get(name, str)
            try:
                return typ(val)
            except (TypeError, ValueError) as exc:
                raise ConfigError(
                    f'Configuration error: cannot convert value "{val}" '
                    f'for variable named "{name}" into type "{typ.__name__}": '
                    f"{exc}"
                )

    def __getattr__(self, name: str) -> Any:
        return self._get(name)

    def __getitem__(self, name: str) -> Any:
        return getattr(self, name)

    @property
    def CAPTCHA_VERIFY_LOCATION(self) -> Optional[Location]:
        """The location of the captcha verification site"""
        overridden_url = self.CAPTCHA_VERIFY_URL
        if overridden_url:
            parsed = urlparse(overridden_url)
            return Location(parsed.hostname, parsed.path)
        return None

    @property
    def LOG_LEVEL(self) -> int:
        name = self._get("LOG_LEVEL").upper()
        if name in _supported_log_level_names:
            return getattr(logging, name)
        else:
            raise ConfigError("Unsupported level name: " + name)

    @property
    def REDIRECT_URL(self) -> str:
        """The URL where the client will be redirected

        Can also be one of the following template tags: REFERER, ORIGIN
        """
        redirect_url = self._get("REDIRECT_URL")
        if "{{" in redirect_url:
            tmpl = Template(redirect_url)
            return tmpl.render(
                ORIGIN=request.headers.get('ORIGIN', '{{ ORIGIN }}'),
                REFERER=request.headers.get('REFERER', '{{ REFERER }}')
            )
        else:
            return redirect_url

    @classmethod
    def get_defaults(cls) -> Dict:
        """List the supported variable names"""
        ns = cls.Defaults.__dict__
        return {k: v for k, v in ns.items() if not k.startswith("__")}


settings = _ConfigurationSettings()
__all__ = (settings.__name__,)
