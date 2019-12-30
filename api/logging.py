from logging import DEBUG, ERROR, INFO, StreamHandler, getLogger

from structlog import configure, get_logger
from structlog.dev import CYAN, ConsoleRenderer
from structlog.processors import (JSONRenderer, StackInfoRenderer, TimeStamper,
                                  UnicodeDecoder, format_exc_info)
from structlog.stdlib import (BoundLogger, LoggerFactory,
                              PositionalArgumentsFormatter, add_log_level,
                              add_logger_name, filter_by_level)

from pythonjsonlogger.jsonlogger import JsonFormatter
from sentry_sdk import init
from sentry_sdk.integrations.logging import LoggingIntegration


class CustomJsonFormatter(JsonFormatter):
    def add_fields(self, log, record, message):
        super().add_fields(log, record, message)
        log["level"] = log.pop("levelname", "").lower()
        log["event"] = log.pop("message", "")


def setup(sentry: str, debug: bool = False) -> None:
    processors = [
        filter_by_level, add_log_level, add_logger_name,
        PositionalArgumentsFormatter(),
        StackInfoRenderer(), format_exc_info,
        UnicodeDecoder()
    ]

    configure(
        logger_factory=LoggerFactory(),
        wrapper_class=BoundLogger,
        cache_logger_on_first_use=True)

    if debug:
        styles = ConsoleRenderer.get_default_level_styles()
        styles['debug'] = CYAN
        processors += [
            TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            ConsoleRenderer(level_styles=styles)
        ]
    else:
        handler = StreamHandler()
        formatter = CustomJsonFormatter("(levelname) (name) (message)")
        handler.setFormatter(formatter)
        getLogger("tornado").addHandler(handler)

        sentry_logging = LoggingIntegration(level=INFO, event_level=ERROR)
        init(sentry, integrations=[sentry_logging])
        processors.append(JSONRenderer())

    handler = StreamHandler()
    configure(processors=processors)
    log = get_logger("api")
    log.addHandler(handler)
    log.propagate = False
    log.setLevel(DEBUG if debug else INFO)
