import http.client
import json

from simple_mailer.config import Config


def is_valid_recaptcha_v3_response(captcha_response: str) -> bool:
    """The given ReCaptcha v3 response has been validated successfully"""
    config = Config()
    host, path = config.CAPTCHA_VERIFY_LOCATION
    params = {"secret": config.CAPTCHA_SECRET, "response": captcha_response}
    headers = {
        "Content-type": "application.json",
        "Accept": "application/json",
    }
    conn = http.client.HTTPSConnection(host)
    conn.request("POST", path, json.dumps(params), headers)
    http_response = conn.getresponse()
    if http_response.status == 200:
        data = json.load(http_response)
        if data["success"]:
            return True
    return False
