"""
Pytest Conftest.py: configure testing environment
"""
from unittest import mock

import pytest

from opinions import core
from opinions.config import Config


@pytest.fixture(scope="session", autouse=True)
def config():
    class TestConfig(Config):
        pass

    return TestConfig


@pytest.fixture(scope='session', autouse=True)
def app(request, config):
    """Session-wide test `Flask` application."""
    settings_override = {
        'TESTING': True,
    }

    _app = core.create_app("opinions-testing",
                           conf=config,
                           start_msg="TEST SESSION STARTED",
                           settings_override=settings_override,
                           use_log_handlers=__name__)

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    def teardown():
        """End Flask app context"""
        ctx.pop()

    request.addfinalizer(teardown)
    return _app


@pytest.fixture()
def client(app):
    """Flask testing client"""
    return app.test_client()


@pytest.fixture(scope='function')
def mocklog(monkeypatch):
    """Access to mock logging object if needed"""
    def mockler(*args, **kwargs):
        """moclog producer"""
        return mockl
    mockl = mock.Mock()
    monkeypatch.setattr(core.logger, "new", mockler)
    return mockl
