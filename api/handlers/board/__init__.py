from .lanes import LanesHandler
from .stations import StationsHandler
from .users import UsersHandler


routes = {
    "lanes": LanesHandler,
    "stations": StationsHandler,
    "users": UsersHandler
}
