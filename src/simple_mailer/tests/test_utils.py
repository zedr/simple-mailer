import logging

from simple_mailer import checks
from simple_mailer.tests.helpers import with_environ_var
from simple_mailer.utils import cloak, get_logger


@with_environ_var("SMTP_PASSWD", "secret")
@with_environ_var("CAPTCHA_SECRET", "secret")
@with_environ_var("CAPTCHA_TYPE", "recaptchav3")
def test_can_cloak_sensitive_vars():
    """Sensitive configuration variables are cloaked to not reveal secrets"""
    cloaked_vars = cloak(checks.get_env_variables())
    assert cloaked_vars["SMTP_PASSWD"] == "********"
    assert cloaked_vars["CAPTCHA_SECRET"] == "********"
    assert cloaked_vars["CAPTCHA_TYPE"] == "recaptchav3"


@with_environ_var("LOG_LEVEL", "critical")
def test_can_configure_logger_correctly():
    log = get_logger("test")
    assert log.level == logging.CRITICAL
