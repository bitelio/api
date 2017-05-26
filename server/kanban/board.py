from ..database import load


class Board:
    def __init__(self, board_id):
        self.cards = load.cards(board_id)
        self.lanes = {lane['Id']: lane for lane in load._get_all_('lanes', board_id)}
        self.stations = load._get_all_('stations', board_id)
        for station in self.stations:
            for lane in station['Lanes']:
                self.lanes[lane]['Station'] = station

    def get_station(self, lane_id):
        lane = self.lanes.get(lane_id)
        if lane:
            return lane.get('Station')
