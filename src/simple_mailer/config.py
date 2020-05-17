import os
from pathlib import Path

# TODO: lazy load using a metaclass?
from typing import List, Optional
from urllib.parse import urlparse

from simple_mailer.http import Location


class Config:
    def __init__(self):
        self.SMTP_HOST: str = os.environ.get("SMTP_HOST", "localhost")
        self._SMTP_PORT: str = os.environ.get("SMTP_PORT", "465")
        self.SMTP_PASSWD: str = os.environ.get("SMTP_PASSWD", "")
        self.SMTP_USERID: str = os.environ.get("SMTP_USERID", "")
        self.MAIL_TO: str = os.environ.get("TO_ADDRESS", "")
        self.MAIL_FROM: str = os.environ.get("FROM_ADDRESS", "")
        self.MAIL_SUBJECT: str = os.environ.get("MAIL_SUBJECT", "")
        self.MAILER_PATH = os.environ.get("MAILER_PATH", "/mail")
        self._USE_TLS: str = os.environ.get("USE_TLS", "true")
        self.MAIL_TEMPLATE_PATH: str = os.environ.get(
            "MAIL_TEMPLATE_PATH",
            (Path(__file__).parent / "templates" / "default.txt").resolve(),
        )
        self.CAPTCHA_TYPE: str = os.environ.get("CAPTCHA_TYPE", "")
        self.CAPTCHA_SECRET: str = os.environ.get("CAPTCHA_SECRET", "")
        self.CAPTCHA_VERIFY_URL: str = os.environ.get("CAPTCHA_VERIFY_URL", "")
        self.REDIRECT_URL: str = os.environ.get("REDIRECT_URL", "")
        self._FIELDS_INCLUDED = os.environ.get("FIELDS_INCLUDED", "")
        self._FIELDS_EXCLUDED = os.environ.get("FIELDS_EXCLUDED", "")

    @property
    def SMTP_PORT(self) -> int:
        try:
            return int(self._SMTP_PORT)
        except ValueError:
            raise ValueError("Invalid port number.")

    @property
    def USE_TLS(self) -> bool:
        return True if self._USE_TLS.lower() == "true" else False

    @property
    def CAPTCHA_VERIFY_LOCATION(self) -> Optional[Location]:
        """The location of the captcha verification site"""
        overridden_url = self.CAPTCHA_VERIFY_URL
        if overridden_url:
            parsed = urlparse(overridden_url)
            return Location(parsed.hostname, parsed.path)
        return None

    @property
    def FIELDS_EXCLUDED(self) -> List[str]:
        """A list of fields that should be ignored

        Note: this overrides FIELDS_INCLUDED."""
        fields = (name.strip() for name in self._FIELDS_EXCLUDED.split(","))
        return [fld for fld in fields if fld]

    @property
    def FIELDS_INCLUDED(self) -> List[str]:
        """A list of fields that should be included"""
        fields = (name.strip() for name in self._FIELDS_INCLUDED.split(","))
        return [fld for fld in fields if fld]
