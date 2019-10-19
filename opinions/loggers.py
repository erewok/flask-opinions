"""
Logging configuration for opinions

"""
import datetime
import logging.config

from pythonjsonlogger import jsonlogger
import structlog

from . import constants
from . import config


def add_app_name_and_vers(logger, log_method, event_dict):
    conf = config.Config()
    event_dict["application"] = conf.app_name
    event_dict["version"] = conf.version
    return event_dict


class JsonLogFormatter(jsonlogger.JsonFormatter):  # pragma: no cover

    _conf = None

    @property
    def conf(self):
        if self._conf is None:
            self._conf = config.Config()
        return self._conf

    def add_fields(self, log_record, record, message_dict):
        """
        This method allows us to inject custom data into resulting log messages
        """
        for field in self._required_fields:
            log_record[field] = record.__dict__.get(field)
        log_record.update(message_dict)

        # Add timestamp and application name if not present
        if "timestamp" not in log_record:
            log_record["timestamp"] = datetime.datetime.utcnow().isoformat()
        if "application" not in log_record:
            log_record["application"] = self.conf.app_name
        if "version" not in log_record:
            log_record["version"] = self.conf.version

        jsonlogger.merge_record_extra(
            record, log_record, reserved=self._skip_fields)


def get_logger(debug=False):
    # For local environments we print to the screen using some colored output.
    # For other environments, we write out JSON logs.
    # We maintain two separate logfiles: INFO and ERROR.
    if debug:
        logging.config.dictConfig({
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "colors": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.dev.ConsoleRenderer(colors=True),
                }
            },
            "handlers": {
                "default": {
                    "level": "INFO",
                    "class": "logging.StreamHandler",
                    "formatter": "colors",
                }
            },
            "loggers": {
                "": {
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": True,
                }
            }
        })
    else:
        logging.config.dictConfig({
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "json": {
                    "class": "opinions.loggers.JsonLogFormatter"
                }
            },
            "handlers": {
                "info": {
                    "level": "INFO",
                    "class": "logging.StreamHandler",
                    "formatter": "json"
                },
                "error": {
                    "level": "ERROR",
                    "class": "logging.StreamHandler",
                    "formatter": "json"
                }
            },
            "loggers": {
                "": {
                    "handlers": ["info", "error"],
                    "level": "INFO",
                    "propagate": True,
                }
            }
        })
    structlog.configure(
        processors=[
            add_app_name_and_vers,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt=constants.LOGGING_TS_FORMAT),
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger()


class FlaskLogger:
    """
    Custom logging object for application
    """

    def __init__(self, config=None, **kwargs):
        self._logger = None
        if config is not None:
            self.init_app(config, **kwargs)

    def init_app(self, is_debug, **kwargs):
        self._logger = get_logger(debug=is_debug)

    def __getattr__(self, item):
        return getattr(self._logger, item)
