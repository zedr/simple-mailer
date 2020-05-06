import os
from pathlib import Path


# TODO: lazy load using a metaclass?
from typing import Tuple, List
from urllib.parse import urlparse

from simple_mailer import constants
from simple_mailer.exceptions import ConfigError


class Config:
    def __init__(self):
        self.SMTP_HOST: str = os.environ.get('SMTP_HOST', 'localhost')
        self._SMTP_PORT: str = os.environ.get('SMTP_PORT', '465')
        self.SMTP_PASSWD: str = os.environ.get('SMTP_PASSWD', '')
        self.SMTP_USERID: str = os.environ.get('SMTP_USERID', '')
        self.MAIL_TO: str = os.environ.get('TO_ADDRESS', '')
        self.MAIL_FROM: str = os.environ.get('FROM_ADDRESS', '')
        self.MAIL_SUBJECT: str = os.environ.get('MAIL_SUBJECT', '')
        self.MAILER_PATH = os.environ.get('MAILER_PATH', '/mail')
        self._USE_TLS: str = os.environ.get('USE_TLS', 'true')
        self.MAIL_TEMPLATE_PATH: str = os.environ.get(
            'MAIL_TEMPLATE_PATH',
            (Path(__file__).parent / 'templates' / 'default.txt').resolve()
        )
        self.CAPTCHA: str = os.environ.get('CAPTCHA', '')
        self.CAPTCHA_SECRET: str = os.environ.get('CAPTCHA_SECRET', '')
        self.CAPTCHA_VERIFY_URL: str = os.environ.get('CAPTCHA_VERIFY_URL', '')
        self._FIELDS_EXCLUDED = os.environ.get('FIELDS_EXCLUDED', '')

    @property
    def SMTP_PORT(self) -> int:
        try:
            return int(self._SMTP_PORT)
        except ValueError:
            raise ValueError('Invalid port number.')

    @property
    def USE_TLS(self) -> bool:
        return True if self._USE_TLS.lower() == 'true' else False

    @property
    def CAPTCHA_VERIFY_LOCATION(self) -> Tuple[str, str]:
        """The location of the captcha verification site"""
        overridden_url = self.CAPTCHA_VERIFY_URL
        if overridden_url:
            parsed = urlparse(overridden_url)
            return (parsed.hostname, parsed.path)
        else:
            if self.CAPTCHA == constants.CaptchaTypes.RECAPTCHA_V3.value:
                return constants.CaptchaVerifyLocations.RECAPTCHA_V3
            else:
                raise ConfigError(
                    f'Captcha type not supported: {self.CAPTCHA}'
                )

    @property
    def FIELDS_EXCLUDED(self) -> List[str]:
        """A list of fields that should be ignored"""
        return self._FIELDS_EXCLUDED.split(',')

