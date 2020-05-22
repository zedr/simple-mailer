import datetime
import json
from urllib.parse import parse_qs

import bottle
from jinja2 import Template, UndefinedError, TemplateError
from simple_mailer import exceptions
from simple_mailer.captcha import CaptchaClient
from simple_mailer.config import settings
from simple_mailer.mailer import Mailer
from simple_mailer.utils import get_logger

log = get_logger(__name__)


class Dispatcher:
    """A controller that processes incoming HTTP requests and sends mail"""

    data: dict
    metadata: dict
    captcha_client: CaptchaClient

    def __init__(self, data=None, metadata=None):
        self.data = {} if data is None else data
        self.metadata = {} if metadata is None else metadata
        self.captcha_client = CaptchaClient.from_environment()

    def process_data(self) -> "Dispatcher":
        """Process the data, applying filters and manipulations appropriately
        """
        data = self.data

        log.debug(f"Received payload: {data}")

        fields_to_include = set(settings.FIELDS_INCLUDED)
        if fields_to_include:
            if self.captcha_client.key:
                fields_to_include.add(self.captcha_client.key)
            data = {k: v for k, v in data.items() if k in fields_to_include}
        fields_to_exclude = settings.FIELDS_EXCLUDED
        if fields_to_exclude:
            data = {
                k: v for k, v in data.items() if k not in fields_to_exclude
            }

        log.debug(f"After filters were applied, the payload was: {data}")

        if not data:
            raise exceptions.SubmittedDataInvalid("Need at least one field")
        self.data = data
        return self

    def parse_request(self, request: bottle.Request) -> "Dispatcher":
        """Extract and store the payload of a given HTTP request"""
        env = request.environ
        content_type = env["CONTENT_TYPE"]
        client_ip = env.get("HTTP_X_FORWARDED_FOR", env.get("REMOTE_ADDR", ""))
        log.info(
            f"Processing HTTP request from client with IP {client_ip} ..."
        )
        self.metadata = {
            "mailer_url": request.url,
            "origin": request.remote_addr or "",
            "client_ip": client_ip,
        }
        body = request.body.read().decode(request.POST.input_encoding)
        if content_type == "application/x-www-form-urlencoded":
            data = {k: (", ").join(v) for k, v in parse_qs(body).items()}
        elif content_type == "application/json":
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                err = log.error("Received invalid JSON")
                log.debug(f"Invalid JSON: {body}")
                raise exceptions.SubmittedDataInvalid(err)
            else:
                log.debug(f"Submitted payload: {data}")
        else:
            err = (
                f"Client sent request unsupported content type: {content_type}"
            )
            log.warning(err)
            raise exceptions.ContentTypeUnsupported(err)
        self.data = data
        self.process_data()
        return self

    def _get_templated_body(self) -> str:
        """Assemble and return the body of the message using the template"""
        tmpl_path = settings.MAIL_TEMPLATE_PATH
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
                err = (
                    f"Cannot open template file. "
                    f"Check if it exists and is readable."
                )
                log.error(err)
                raise exceptions.ConfigError(err)
        else:
            return json.dumps(self.data)

    def get_server(self) -> Mailer:
        """Get an instance of the mailer server"""
        return Mailer(
            host=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            use_tls=settings.USE_TLS,
        )

    def dispatch(self) -> None:
        """Dispatch a given HTTP request

        Returns true or false depending on the outcome.
        """
        self.captcha_client.validate_data(self.data)

        self.metadata.update(
            timestamp_utc=datetime.datetime.utcnow().isoformat()
        )

        cfg = {
            "from_": settings.FROM_ADDRESS,
            "to": settings.TO_ADDRESS,
            "subject": self.get_subject(),
            "body": self._get_templated_body(),
        }
        self.get_server().connect().send_message(**cfg).disconnect()
        log.info(
            f"Sent email to server {settings.SMTP_HOST}:{settings.SMTP_PORT}"
        )

    def get_subject(self) -> str:
        """Get the subject for the current email"""
        subject = settings.MAIL_SUBJECT
        if subject:
            tmpl = Template(subject)
            return tmpl.render(data=self.data, metadata=self.metadata)
        else:
            return subject
