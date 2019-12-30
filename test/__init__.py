from tornado.testing import AsyncHTTPTestCase

from api.models import Role, User
from api.server import setup
from api.services import Services
from api.settings import ServicesSettings, TornadoSettings
from rapidjson import dumps


class BaseTestCase(AsyncHTTPTestCase):
    def setUp(self):
        async def start():
            await Services.start(ServicesSettings(store="sqlite://:memory:"))
            await User.create(**self.user())
            Services.redis.set(*self.session())

        super().setUp()
        self.io_loop.run_sync(start)

    def user(self):
        password = ("$argon2id$v=19$m=102400,t=2,p=8$vVdqLeV"
                    "cay2ldO4do5QSQg$aIEv9g7o640tjqT9h3oXrw")
        return {
            "username": 'admin',
            "email": "admin@bitelio.com",
            "role": Role.admin,
            "password": password,
        }

    def session(self):
        return ('+++', ('{"username": "admin", "token": "+++",'
                        ' "role": 3, "date": "2000-01-01 00:00:00"}'))

    @staticmethod
    def get_app():
        settings = TornadoSettings(
            debug=False, cookie_secret="", xsrf_cookies=False)
        return setup(settings)

    def get(self, url=None, auth=False, **kwargs):
        if auth:
            headers = kwargs.get('headers', {})
            headers.update({'Cookie': 'token=+++'})
            kwargs['headers'] = headers
        return self.fetch(url or self.url, **kwargs)

    def post(self, body):
        return self.get(self.url, method="POST", body=dumps(body))

    def delete(self):
        return self.get(method="DELETE")

    def tearDown(self):
        self.io_loop.run_sync(Services.stop)
        super().tearDown()
