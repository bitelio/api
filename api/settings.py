from pydantic import BaseSettings


class ConfigurationError(Exception):
    pass


class SettingsConfig(BaseSettings):
    class Config():
        env_prefix = 'btl_'


class ServerSettings(SettingsConfig):
    address: str = "0"
    port: int = 80


class ServicesSettings(SettingsConfig):
    cache: str = ""
    store: str = ""
    sentry: str = ""


class TornadoSettings(SettingsConfig):
    compress_response: bool = True
    cookie_secret: str = ""
    debug: bool = False
    xsrf_cookies: bool = True


class Settings:
    server: ServerSettings
    services: ServicesSettings
    tornado: TornadoSettings

    def __init__(self):
        for service, cls in self.__annotations__.items():
            setattr(self, service, cls())

    @property
    def debug(self):
        return self.tornado.debug
