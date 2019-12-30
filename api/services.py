from redis import Redis
from structlog import get_logger
from tortoise import Tortoise

from .settings import ServicesSettings


class Services:
    redis: Redis

    @classmethod
    async def start(cls, settings: ServicesSettings) -> None:
        log.info("Starting services")
        if settings.cache:
            cls.redis = Redis(settings.cache)
        else:
            from fakeredis import FakeRedis
            cls.redis = FakeRedis()
        try:
            cls.redis.get('')
            log.info(f"Connected to cache on {settings.cache or 'localhost'}")
            await Tortoise.init(
                db_url=settings.store, modules={'models': ['api.models']})
            log.info(f"Connected to database on {settings.store}")
            await Tortoise.generate_schemas(safe=True)
        except Exception as error:
            log.critical(error)
            exit(1)

    @classmethod
    async def stop(cls):
        log.info("Stopping services")
        cls.redis.close()
        await Tortoise.close_connections()


log = get_logger(__name__)
