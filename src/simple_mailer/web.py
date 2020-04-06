import os

import bottle

from simple_mailer.mailer import Mailer


class Config:
    def __init__(self):
        self.SMTP_HOST: str = os.environ.get("SMTP_HOST", "localhost")
        self._SMTP_PORT: str = os.environ.get("SMTP_PORT", "465")
        self.SMTP_PASSWD: str = os.environ.get("SMTP_PASSWD", "")
        self.SMTP_USERID: str = os.environ.get("SMTP_USERID", "")
        self.MAIL_TO: str = os.environ.get("TO_ADDRESS", "")
        self.MAIL_FROM: str = os.environ.get("FROM_ADDRESS", "")
        self.MAIL_SUBJECT: str = os.environ.get("MAIL_SUBJECT", "")
        self._USE_TLS: str = os.environ.get("USE_TLS", "true")

    @property
    def SMTP_PORT(self) -> int:
        try:
            return int(self._SMTP_PORT)
        except ValueError:
            raise ValueError("Invalid port number.")

    @property
    def USE_TLS(self) -> bool:
        return True if self._USE_TLS.lower() == "true" else False


@bottle.post("/mail")
def mail():
    try:
        config = Config()
    except ValueError:
        bottle.response.status_code = 500
        return "Server configuration error: {err.message}"

    server = Mailer(
        host=config.SMTP_HOST, port=config.SMTP_PORT, use_tls=config.USE_TLS
    )
    server.connect()
    server.send_message(
        from_=config.MAIL_FROM,
        to=config.MAIL_TO,
        subject=config.MAIL_SUBJECT,
        body="test",
    )
    server.disconnect()
    return f"Hello world! {config.MAIL_TO}"


def get_application():
    return bottle.default_app()
