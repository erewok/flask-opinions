"""
Pytest Conftest.py: configure testing environment
"""
import os
from unittest import mock

import pytest

from opinions import core
from opinions import config as proj_config


test_dir = os.path.dirname(__file__)
fixtures = os.path.join(test_dir, "fixtures")


@pytest.fixture(scope="session", autouse=True)
def make_secrets():
    secrets = {}

    for idx, secret_file in enumerate(proj_config.secret_keys):
        value = f"SECRET_{secret_file}_{idx}"
        secrets[secret_file] = value
        with open(os.path.join(fixtures, secret_file), "w") as fl:
            fl.write(value)
    return secrets


@pytest.fixture(autouse=True, scope="session")
def clobber_secrets_dir():
    old_dir = os.getenv("OPINIONS_SECRETS_DIR")
    os.environ["OPINIONS_SECRETS_DIR"] = fixtures
    yield
    if old_dir is None:
        old_dir = ""
    os.environ["OPINIONS_SECRETS_DIR"] = old_dir


@pytest.fixture(scope="session", autouse=True)
def config(make_secrets):
    class TestConfig(proj_config.Config):
        is_debug: bool = False
        version: str = "0.0.1-test"
        environment: str = "testing!"
        app_name: str = "testing-opinions"

        # redis connection
        redis_host: str = ""
        redis_port: str = ""
        redis_db: str = "0"

        # secrets should go in secrets_dir
        secrets_dir: str = ""
        redis_passwd: str = "SECRET!"
        something_secret: str = "SECRET!"
        REDIS_CONN_STR = ""

    return TestConfig()


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


@pytest.fixture
def json_ct():
    return {"Content-Type": "application/json"}
