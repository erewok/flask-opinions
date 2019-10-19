"""
core.py: Create a flask.Flask App object for running  the opinions project
"""
import logging

from flask import Flask

from . import config
from . import constants
from . import loggers

logger = loggers.FlaskLogger()   # noqa


def create_app(package_name,
               conf=None,
               use_log_handlers="gunicorn.info",
               start_msg=f"{constants.APPLICATION_NAME} API started",
               settings_override=None):
    """Flask App `create_app` pattern for arbitrary Flask Apps"""
    if conf is None:
        conf = config.Config()

    app = Flask(package_name, instance_relative_config=True)

    app.config.from_object(conf)
    if settings_override is not None:
        app.config.update(settings_override)  # useful for testing

    # No lowercased values set on config...
    for attr in dir(conf):
        if "__" not in attr:
            app.config[attr] = getattr(conf, attr)

    # Inits various libraries

    # others
    logger.init_app(conf.is_debug)

    # Configure logging
    if use_log_handlers is not None:
        requested_logger = logging.getLogger(use_log_handlers)
        app.logger.handlers = requested_logger.handlers[:]

    log = logger.new()
    log.info(start_msg, environment=conf.environment)

    # Register blueprints (avoiding standard Flask circular imports...)
    from .endpoints import base
    app.register_blueprint(base.Base)

    return app
