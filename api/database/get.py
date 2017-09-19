def trt_by_lane(query):
    """ Returns the sum of TRT per lane """
    pass


def total_cards_by_type(query):
    """ Returns the number of cards grouped by type """
    pass


def tag_events(query):
    """ List of tag events """
    pass


def comment_events(query):
    """ List of comment events """
    pass


def move_events(query):
    """ """
    pass


class Events:
    def comments(self):
        pass

    def tags(self):
        pass


class Stations:
    schema = "schemas.station"

    def trt(self, query):
        events = self.events.trt(query)
        stations = self.get(query)
        return [trt for trt in events if trt in stations]

    def get(self):
        """ Get stations """
        pass


class Lanes:
    def wip(self):
        """ Only wip lanes """
        pass

    def get(self):
        pass
