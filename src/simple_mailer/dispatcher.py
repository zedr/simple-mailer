import json

import bottle

from simple_mailer.exceptions import ConfigError
from simple_mailer.mailer import Mailer
from simple_mailer.config import Config


class Dispatcher:
    """A controller that processes incoming HTTP requests and sends mail"""

    @classmethod
    def dispatch(self, message: dict) -> None:
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
            body=json.dumps(message),
        )
        server.disconnect()
