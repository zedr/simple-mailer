class BaseSimpleMailerException(Exception):
    """Base exception for package Simple Mailer"""


class ConfigError(BaseSimpleMailerException):
    """A configuration error has occurred"""
