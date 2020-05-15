import http.client
import json
from dataclasses import dataclass
from typing import Dict

from simple_mailer import exceptions
from simple_mailer.config import Config
from simple_mailer.http import Location


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
            raise exceptions.MissingCaptchaResponse(
                f"The expected response for "
                f"captcha protocol '{self.protocol_name}' was not found. "
                f"Expected a field named {self.key}."
            )

    def validate_data(self, data: Dict) -> None:
        """Introspect the given data to infer and validate the response"""
        pass

    @staticmethod
    def from_environment() -> "CaptchaClient":
        """Choose and create a captcha client by introspecting the environment
        """
        config = Config()
        protocol = config.CAPTCHA_TYPE
        if not protocol:
            return CaptchaClient()
        elif protocol == Recaptchav3Client.protocol_name:
            loc = config.CAPTCHA_VERIFY_LOCATION
            if loc is None:
                return Recaptchav3Client()
            else:
                return Recaptchav3Client(location=loc)
        else:
            raise exceptions.UnknownCaptchaProtocol(
                f"Configuration Error: unsupported Captcha protocol: "
                f"{protocol}"
            )


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
        config = Config()
        resp = self.extract_response(data)
        params = {"secret": config.CAPTCHA_SECRET, "response": resp}
        headers = {
            "Content-type": "application.json",
            "Accept": "application/json",
        }
        conn = http.client.HTTPSConnection(self.location.hostname)
        conn.request("POST", self.location.path, json.dumps(params), headers)
        http_response = conn.getresponse()
        if http_response.status == 200:
            data = json.load(http_response)
            if data["success"]:
                return None
            else:
                raise exceptions.InvalidCaptchaResponse(
                    f"The POST request did not contain the correct response. "
                    f"The POST data should include the response using a key "
                    f'named "{self.key}" and a value for it.'
                )
        raise exceptions.FailedCaptchaResponse(
            f"The captcha response verification has failed. "
            f"The challenge response provided in the POST data was: {resp}"
        )
