import os
from pathlib import Path
from typing import Optional, Any
from urllib.parse import urlparse

from simple_mailer.exceptions import ConfigError
from simple_mailer.http import Location


class BoolStr:
    """A factory class that can construct booleans from strings"""

    def __new__(cls, value, *args, **kwargs):
        if hasattr(value, "lower"):
            return bool(value.lower() == "true")
        else:
            return bool(value)


class SetStr:
    sep = ","

    def __new__(cls, value, *args, **kwargs):
        if value and hasattr(value, "split"):
            return frozenset(value.split(cls.sep))
        else:
            return frozenset(value)


class _ConfigValueTypeChecker(type):
    """Check that the type definitions for the given class are supported"""

    supported_types = (int, float, str, bytes, bool, BoolStr, tuple, SetStr)

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

        Only the following primitive types are supported: str, int, float
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
        FIELDS_INCLUDED: SetStr = SetStr("")
        FIELDS_EXCLUDED: SetStr = SetStr("")

    def _get(self, name: str) -> Any:
        val = os.environ.get(name, getattr(self.Defaults, name))
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


settings = _ConfigurationSettings()
