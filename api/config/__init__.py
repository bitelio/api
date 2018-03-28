from api.auth import AuthHandler
from api.user import UserHandler
from api.board import BoardHandler
from api.board.lanes import LanesHandler
from api.board.users import UsersHandler
from api.board.settings import SettingsHandler
from api.board.stations import StationsHandler


routes = [
    ('/api/auth', AuthHandler),
    ('/api/auth', UserHandler),
    ('/api/board', BoardHandler),
    ('/api/board/lanes', LanesHandler),
    ('/api/board/users', UsersHandler),
    ('/api/board/settings', SettingsHandler),
    ('/api/board/stations', StationsHandler)
]
