class BaseSimpleMailerException(Exception):
    """Base exception for package Simple Mailer"""


class ConfigError(BaseSimpleMailerException):
    """A configuration error has occurred"""


class ContentTypeUnsupported(BaseSimpleMailerException):
    """The submitted data is formatted using an unsupported content type"""


class InvalidCaptchaResponse(BaseSimpleMailerException):
    """The captcha response key/value pair is invalid or missing"""


class FailedCaptchaResponse(BaseSimpleMailerException):
    """The captcha response verification with the server has failed"""


class SubmittedDataInvalid(BaseSimpleMailerException):
    """The submitted data is invalid"""


class MailServerError(BaseSimpleMailerException):
    """Got an error from the remote SMTP server"""
