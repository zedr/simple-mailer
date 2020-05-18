import pytest
from simple_mailer.config import settings, BoolStr, SetStr
from simple_mailer.exceptions import ConfigError
from simple_mailer.tests.helpers import with_environ_var


def test_bool_str_type():
    assert BoolStr("False") is False
    assert BoolStr("false") is False
    assert BoolStr("True") is True
    assert BoolStr("true") is True
    assert BoolStr("") is False
    assert BoolStr("abc") is False
    assert BoolStr(True) is True
    assert BoolStr(False) is False


def test_list_str_type():
    assert SetStr("a,b,c") == frozenset(("a", "b", "c"))
    assert SetStr("a") == {"a"}
    assert SetStr([]) == frozenset()
    assert SetStr("") == frozenset()


@with_environ_var("SMTP_PORT", 4465)
def test_lazy_loaded_config():
    assert settings.SMTP_PORT == 4465


@with_environ_var("SMTP_PORT", "invalid")
def test_invalid_numeric_variable_value_raises_config_error():
    with pytest.raises(ConfigError):
        assert settings.SMTP_PORT == 465


@with_environ_var("USE_TLS", "false")
def test_with_bool_string_false():
    assert not settings.USE_TLS
