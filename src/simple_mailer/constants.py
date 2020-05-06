from enum import Enum


class CaptchaTypes(Enum):
    """An enumeration of the supported types of Captcha"""

    RECAPTCHA_V3 = "recaptchav3"

    @property
    def values_as_str(self) -> str:
        """Return the printed list of values"""
        return ", ".join(el.value for el in list(self))

    def __iter__(self):
        return iter(self)


class CaptchaResponseKeys:
    """The key names of the Captcha responses"""

    RECAPTCHA_V3 = "g-recaptcha-response"


class CaptchaVerifyLocations:
    """The URL of the captcha verification endpoints"""

    RECAPTCHA_V3 = ("www.google.com", "/recaptcha/api/siteverify")
