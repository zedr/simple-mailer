import json
from dataclasses import dataclass
from typing import Optional
from urllib.parse import parse_qs

import bottle

from jinja2 import Template

from simple_mailer.config import Config
from simple_mailer.exceptions import ConfigError
from simple_mailer.mailer import Mailer


@dataclass
class Dispatcher:
    '''A controller that processes incoming HTTP requests and sends mail'''
    data: Optional[dict] = None

    def __post_init__(self):
        self._config = Config()

    def parse_request(self, request: bottle.Request) -> 'Dispatcher':
        '''Extract and store the payload of a given HTTP request'''
        body = request.body.read().decode('utf8')
        content_type = request.environ['CONTENT_TYPE']
        if content_type == 'application/x-www-form-urlencoded':
            self.data = parse_qs(body)
        else:
            self.data = json.loads(body)
        return self

    @property
    def template_path(self) -> str:
        return self._config.MAIL_TEMPLATE_PATH

    def _get_templated_body(self) -> str:
        '''Assemble and return the body of the message using the template'''
        tmpl_path = self.template_path
        if tmpl_path:
            try:
                with open(tmpl_path) as fd:
                    tmpl = Template(fd.read())
                    return tmpl.render(data=self.data)
            except IOError:
                raise ConfigError(
                    f'Cannot open template file. '
                    f'Check if it exists and is readable.'
                )
        else:
            return json.dumps(self.data)


    def dispatch(self) -> None:
        '''Dispatch a given HTTP request

        Returns true or false depending on the outcome.
        '''
        try:
            config = Config()
        except ValueError:
            bottle.response.status_code = 500
            raise ConfigError('Mailer server application configuration error')

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
