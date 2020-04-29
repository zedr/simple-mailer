class BaseSimpleMailerException(Exception):
    """Base exception for package Simple Mailer"""


class ConfigError(BaseSimpleMailerException):
    """A configuration error has occurred"""


class ContentTypeUnsupported(BaseSimpleMailerException):
    """The submitted data is formatted using an unsupported content type"""
