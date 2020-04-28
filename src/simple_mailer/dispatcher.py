import json
from dataclasses import dataclass
from typing import Optional
from urllib.parse import parse_qs

import bottle
from simple_mailer.config import Config
from simple_mailer.exceptions import ConfigError
from simple_mailer.mailer import Mailer


@dataclass
class Dispatcher:
    """A controller that processes incoming HTTP requests and sends mail"""
    data: Optional[dict] = None

    def parse_request(self, request: bottle.Request) -> 'Dispatcher':
        """Extract and store the payload of a given HTTP request"""
        body = request.body.read().decode("utf8")
        content_type = request.environ["CONTENT_TYPE"]
        if content_type == "application/x-www-form-urlencoded":
            self.data = parse_qs(body)
        else:
            self.data = json.loads(body)
        return self

    def dispatch(self) -> None:
        """Dispatch a given HTTP request

        Returns true or false depending on the outcome.
        """
        try:
            config = Config()
        except ValueError:
            bottle.response.status_code = 500
            raise ConfigError("Mailer server application configuration error")

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
            body=json.dumps(self.data),
        )
        server.disconnect()
