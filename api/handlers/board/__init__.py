from .board import BoardHandler
from .lanes import LanesHandler
from .card_types import CardTypesHandler
from .classes_of_service import ClassesOfServiceHandler
from .stations import StationsHandler
from .users import UsersHandler


routes = {
    "": BoardHandler,
    "lanes": LanesHandler,
    "card_types": CardTypesHandler,
    "classes_of_service": ClassesOfServiceHandler,
    "stations": StationsHandler,
    "users": UsersHandler
}
