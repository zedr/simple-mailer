import datetime
import json
from urllib.parse import parse_qs

import bottle
from jinja2 import Template, UndefinedError, TemplateError
from simple_mailer import constants
from simple_mailer import exceptions
from simple_mailer.captcha import is_valid_recaptcha_v3_response
from simple_mailer.config import Config
from simple_mailer.mailer import Mailer


class Dispatcher:
    """A controller that processes incoming HTTP requests and sends mail"""

    data: dict
    metadata: dict

    def __init__(self, data=None, metadata=None):
        self._config = Config()
        self.data = {} if data is None else data
        self.metadata = {} if metadata is None else metadata

    def parse_request(self, request: bottle.Request) -> "Dispatcher":
        """Extract and store the payload of a given HTTP request"""
        body = request.body.read().decode("utf8")
        env = request.environ
        content_type = env["CONTENT_TYPE"]
        client_ip = env.get("HTTP_X_FORWARDED_FOR", env.get("REMOTE_ADDR", ""))
        if content_type == "application/x-www-form-urlencoded":
            data = parse_qs(body)
        elif content_type == "application/json":
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                raise exceptions.SubmittedDataInvalid("Invalid JSON")
        else:
            raise exceptions.ContentTypeUnsupported(
                f"Cannot process content type: {content_type}"
            )

        fields_to_include = self._config.FIELDS_INCLUDED
        if fields_to_include:
            data = {k: v for k, v in data.items() if k in fields_to_include}

        fields_to_exclude = self._config.FIELDS_EXCLUDED
        if fields_to_exclude:
            data = {
                k: v for k, v in data.items() if k not in fields_to_exclude
            }

        if not data:
            raise exceptions.SubmittedDataInvalid("Need at least one field")

        self.data = data
        self.metadata = {
            "mailer_url": request.url,
            "origin": request.remote_addr or "",
            "client_ip": client_ip,
        }
        return self

    @property
    def template_path(self) -> str:
        """The path to the template file"""
        return self._config.MAIL_TEMPLATE_PATH

    def _get_templated_body(self) -> str:
        """Assemble and return the body of the message using the template"""
        tmpl_path = self.template_path
        if tmpl_path:
            try:
                with open(tmpl_path) as fd:
                    tmpl = Template(fd.read())
                    try:
                        return tmpl.render(
                            data=self.data, metadata=self.metadata
                        )
                    except UndefinedError as exc:
                        raise TemplateError(
                            f"The template did not define the required fields:"
                            f" {exc.message}"
                        )
            except IOError:
                raise exceptions.ConfigError(
                    f"Cannot open template file. "
                    f"Check if it exists and is readable."
                )
        else:
            return json.dumps(self.data)

    def check_captcha(self) -> None:
        """Verify that the captcha challenge was responded correctly

        If the captchas are not configured (using environment variables) this
        is a no-op."""
        captcha = self._config.CAPTCHA
        if not captcha:
            pass
        elif captcha == "recaptchav3":
            captcha_key = constants.CaptchaResponseKeys.RECAPTCHA_V3
            try:
                resp = self.data.pop(captcha_key)
            except KeyError:
                raise exceptions.InvalidCaptchaResponse(
                    f"The POST request did not contain the correct response. "
                    f"The POST data should include the response using a key "
                    f'named "{captcha_key}" and a value for it.'
                )
            else:
                if resp:
                    if not is_valid_recaptcha_v3_response(resp):
                        raise exceptions.FailedCaptchaResponse(
                            f"The captcha response verification has failed. "
                            f"The challenge response provided in the POST "
                            f"data was: {resp}"
                        )
                else:
                    raise exceptions.InvalidCaptchaResponse(
                        f"Missing value for POST data key {captcha_key}"
                    )
        else:
            raise exceptions.ConfigError(
                f'Unsupported captcha type: "{captcha}". '
                f"Supported types are: {constants.CaptchaTypes.values_as_str}"
            )

    def dispatch(self) -> None:
        """Dispatch a given HTTP request

        Returns true or false depending on the outcome.
        """
        try:
            config = Config()
        except ValueError:
            bottle.response.status_code = 500
            raise exceptions.ConfigError(
                "Mailer server application configuration error"
            )

        self.check_captcha()

        self.metadata.update(
            timestamp_utc=datetime.datetime.utcnow().isoformat()
        )

        server = Mailer(
            host=config.SMTP_HOST,
            port=config.SMTP_PORT,
            use_tls=config.USE_TLS,
        )
        server.connect()
        server.send_message(
            from_=config.MAIL_FROM,
            to=config.MAIL_TO,
            subject=config.MAIL_SUBJECT,
            body=self._get_templated_body(),
        )
        server.disconnect()
