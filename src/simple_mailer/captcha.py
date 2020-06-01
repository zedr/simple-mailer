import http.client
import json
from dataclasses import dataclass
from typing import Dict
from urllib.parse import urlencode

from simple_mailer import exceptions
from simple_mailer.config import settings
from simple_mailer.http import Location
from simple_mailer.utils import get_logger

log = get_logger(__name__)


@dataclass
class CaptchaClient:
    """An generic object that verifies a given captcha response
    """

    protocol_name: str = "noop"
    key: str = ""
    location = None

    def extract_response(self, data: Dict) -> str:
        """Extract the correct response from"""
        try:
            return data[self.key]
        except KeyError:
            err = (
                f"The expected response for "
                f"captcha protocol '{self.protocol_name}' was not found. "
                f"Expected a field named {self.key}."
            )
            log.error(err)
            raise exceptions.MissingCaptchaResponse(err)

    def validate_data(self, data: Dict) -> None:
        """Introspect the given data to infer and validate the response"""
        pass

    @staticmethod
    def from_environment() -> "CaptchaClient":
        """Choose and create a captcha client by introspecting the environment
        """
        protocol = settings.CAPTCHA_TYPE
        if not protocol:
            log.debug("No captcha protocol configured for use")
            return CaptchaClient()
        elif protocol == Recaptchav3Client.protocol_name:
            loc = settings.CAPTCHA_VERIFY_LOCATION
            if loc is None:
                client = Recaptchav3Client()
            else:
                client = Recaptchav3Client(location=loc)
            log.debug(
                f"Using captcha protocol {client.protocol_name} with "
                f"verification URL at {client.location.https_url}"
            )
            return client
        else:
            err = (
                f"Configuration Error: unsupported Captcha protocol: "
                f"{protocol}"
            )
            log.error(err)
            raise exceptions.UnknownCaptchaProtocol(err)


@dataclass
class Recaptchav3Client(CaptchaClient):
    """A Recaptchav3 client"""

    protocol_name: str = "recaptchav3"
    key: str = "g-recaptcha-response"
    location: Location = Location(
        "www.google.com", "/recaptcha/api/siteverify"
    )

    def validate_data(self, data: Dict) -> None:
        """Connect to the server and validate the given response"""
        resp = self.extract_response(data)
        params = {"secret": settings.CAPTCHA_SECRET, "response": resp}
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        log.debug(f"Validating catpcha response data: {params}")
        conn = http.client.HTTPSConnection(self.location.hostname)
        log.debug(
            f"Sending captcha verification POST request to "
            f"{self.location.https_url} ..."
        )
        try:
            conn.request(
                "POST", self.location.https_url, urlencode(params), headers
            )
        except ConnectionRefusedError as exc:
            raise exceptions.CaptchaServerConnectionRefused(
                f'Could not connect to the Captcha server '
                f'at "{self.location.path}", reason: {exc}'
            )
        http_response = conn.getresponse()
        log.debug(f"Got {http_response.status} response from catpcha server.")
        if http_response.status == 200:
            data = json.load(http_response)
            if data["success"]:
                log.debug(f"Captcha response was validated successfully.")
                return None
            else:
                err = (
                    f"Captcha response failed validation"
                )
                log.debug(err)
                log.debug(f'Got this data from server: {data}')
                log.warning("Client failed captcha verification.")
                raise exceptions.InvalidCaptchaResponse(err)
        err = (
            f"The captcha response verification has failed. "
            f"The challenge response provided in the POST data was: {resp}"
        )
        log.debug(err)
        log.warning("Client failed captcha verification.")
        raise exceptions.FailedCaptchaResponse(err)
