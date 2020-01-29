from signal import SIGTERM, SIGINT
from asyncio import get_event_loop, ensure_future
from structlog import get_logger

from tornado.web import Application

from . import logging
from .services import Services
from .settings import Settings, TornadoSettings
from .handlers import NotFoundHandler, handler_log, routes


def setup(settings: TornadoSettings) -> Application:
    return Application(
        routes,  # type: ignore
        default_handler_class=NotFoundHandler,
        log_function=handler_log,
        **settings.dict())


def start() -> None:
    settings = Settings()
    logging.setup(settings.services.sentry, settings.debug)
    loop = get_event_loop()
    loop.run_until_complete(Services.start(settings.services))
    log.info(f"Starting API server")
    application = setup(settings.tornado)
    server = application.listen(**settings.server.dict())
    for signal in [SIGINT, SIGTERM]:
        loop.add_signal_handler(signal, lambda: stop(server, loop))
    log.info(f"Listening on {settings.server.port}")
    loop.run_forever()


def stop(server, loop) -> None:
    log.info(f'Stopping server')
    server.stop()
    ensure_future(Services.stop())
    loop.call_later(1, loop.stop)


log = get_logger(__name__)
