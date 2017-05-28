from datetime import datetime
from cached_property import cached_property

import officehours
from . import kanban


class Move:
    def __init__(self, data):
        self.date_in = data
        self.date_out = data
        self.lane = data
        self.station = None
        self.phase = None
        self.next = None
        self.previous = None

    @cached_property
    def time(self):
        return self.date_out - self.date_in

    @cached_property
    def trt(self):
        # return timer.workinghours(self.date_in, self.date_out or datetime.now())
        return 0


class Card(kanban.Card):
    @cached_property
    def timeline(self):
        """ Returns a list of card movements including the time elapsed among them """
        timeline = [move for move in self.moves if move['out']]
        for move in timeline:
            move['time'] = (move['out'] - move['in']).total_seconds() / 3600
            move['trt'] = self.board.timer.working_hours(move['in'], move['out'])
        return timeline

    @cached_property
    def lanes(self):
        """ Returns a dictionary containing the time data for the
        lanes the card has been through. Doesn't consider the
        time spent in the current one """
        lanes = {}
        for event in self.timeline:
            lane = event['lane']
            if lane in lanes:
                lanes[lane]['trt'] += event['trt']
                lanes[lane]['time'] += event['time']
                lanes[lane]['out'] = event['out']
                lanes[lane]['events'] += 1
            else:
                lanes[lane] = {'in': event['in'],
                               'out': event['out'],
                               'time': event['time'],
                               'trt': event['trt'],
                               'events': 1}
        return lanes

    @cached_property
    def stations(self):
        """ Returns a dictionary containing the time data for the
        stations the card has been through. Doesn't consider the
        time spent in the current one """
        stations = {}
        for lane, data in self.lanes.items():
            station = lane.station if lane else None
            if station in stations:
                stations[station]['trt'] += data['trt']
                stations[station]['time'] += data['time']
                stations[station]['out'] = data['out']
                stations[station]['events'] += data['events']
            else:
                stations[station] = {'in': data['in'],
                                     'out': data['out'],
                                     'time': data['time'],
                                     'trt': data['trt'],
                                     'events': data['events']}
        return stations

    @cached_property
    def phases(self):
        """ Returns a dictionary containing the time data for the
        phases the card has been through. Doesn't consider the
        time spent in the current one """
        phases = {}
        for station, data in self.stations.items():
            phase = station.phase if station else None
            if phase in phases:
                phases[phase]['trt'] += data['trt']
                phases[phase]['time'] += data['time']
                phases[phase]['out'] = data['out']
                phases[phase]['events'] += data['events']
            else:
                phases[phase] = {'in': data['in'],
                                 'out': data['out'],
                                 'time': data['time'],
                                 'trt': data['trt'],
                                 'events': data['events']}
        return phases

    @cached_property
    def trt(self, hours=False):
        """ Total time the card has spent in all stations together """
        total = 0
        for move in self.moves:
            if move['lane'] and move['lane'].station:
                if hours:
                    total += self.board.timer.working_hours(move['in'], move['out'] or datetime.now())
                else:
                    total += ((move['out'] or datetime.now()) - move['in']).total_seconds() / 3600
        return total

    @cached_property
    def expectation(self):
        """ Expected total working hours required to archive the card """
        pass
        # total = 0

    @cached_property
    def start_date(self):
        """ Date in which the card was first moved into a station """
        start_date = None
        for move in self.moves:
            if not start_date and move['lane'] and move['lane'].station:
                start_date = move['in']
            elif move['lane'] and 'major changes' in move['lane'].title.lower():
                self._major_changes_ = True
                start_date = move['in']
        return start_date

    @property
    def station(self):
        """ Returns the current station """
        return self.lane.station

    @property
    def phase(self):
        """ Returns the current phase """
        if self.station:
            return self.station.phase

    def trt_lane(self, lane=None, hours=False):
        """ Returns the TRT for a given lane, including the current one

        :param int lane: Id number of the lane. Default to current lane
        :param bool hours: If True, returns the TRT in working hours
        """
        total = 0
        if not lane:
            lane = self.lane
        elif isinstance(lane, int):
            lane = self.board.lanes[lane]
        for move in self.moves:
            if move['in'] < self.start_date:
                continue
            if move['lane'] and move['lane'].id == lane.id:
                if hours:
                    total += self.board.timer.working_hours(move['in'], move['out'] or datetime.now())
                else:
                    total += ((move['out'] or datetime.now()) - move['in']).total_seconds() / 3600
        return total

    def trt_station(self, station=None, hours=False):
        """ Returns the TRT for a given station, including the current one

        :param int station: Position of the station. Defaults to current station
        :param bool hours: If True, returns the TRT in working hours
        """
        if self.station:
            total = 0
            if not station:
                station = self.station
            elif isinstance(station, int):
                station = self.board.stations[station]
            for lane in station.lanes:
                total += self.trt_lane(lane.id, hours)
            return total

    def trt_phase(self, phase, hours=False):
        """ Returns the TRT for a given phase, including the current one

        :param int phase: Position of the phase
        :param bool hours: If True, returns the TRT in working hours
        """
        total = 0
        if isinstance(phase, int):
            phase = self.board.phases[phase]
        for station in phase.stations:
            total += self.trt_station(station.id, hours)
        return total

    def ect_station(self):
        """ Returns the estimated completion date for the current station """
        if self.station:
            remaining = self.station.target(self) - self.trt_station(self.station.id, hours=True)
            remaining = max(remaining, 0)
            return self.board.timer.due_date(remaining, datetime.now())

    def ect_phase(self):
        """ Returns the estimated completion date for the current phase """
        if self.station and self.station.phase:
            remaining = self.station.phase.target(self) - self.trt_phase(self.station.phase.id, hours=True)
            return self.board.timer.due_date(remaining, datetime.now())

    def target_station(self, station=None):
        """ Returns the target TRT for a given station

        :param int station: Position of the station. Defaults to current station
        """
        if station:
            if isinstance(station, int):
                return self.board.stations[station].target(self)
            else:
                return station.target(self)
        else:
            if self.station:
                return self.station.target(self)

    @cached_property
    def plan(self):
        """ Returns all the initially planned completion dates for each station """
        plan = {}
        ect = self.start_date or datetime.now()
        for position in range(1, max(self.board.stations)+1):
            station = self.board.stations[position]
            target = station.target(self)
            ect = self.board.timer.due_date(target, ect)
            plan[position] = {'station': station, 'target': target, 'ect': ect}
        return plan

    @cached_property
    def estimation(self):
        """ Returns all the predicted completion dates for each remaining station """
        # TODO: estimation from the last known lane
        estimation = {}
        if self.station:
            consumed = self.trt_station(self.station.id, hours=True)
            target = self.station.target(self)
            ect = self.board.timer.due_date(target - consumed, datetime.now())
            estimation[self.station.id] = {'station': self.station, 'target': target, 'ect': ect}
            for position in range(self.station.id+1, max(self.board.stations)+1):
                station = self.board.stations[position]
                target = station.target(self)
                ect = self.board.timer.due_date(target, ect)
                estimation[position] = {'station': station, 'target': target, 'ect': ect}
        return estimation

    @cached_property
    def completed_stations(self):
        """ Returns a list of completed stations """
        data = {}
        for move in self.moves:
            if move['lane'] and move['lane'].station and move['out']:
                time = self.board.timer.working_hours(move['in'], move['out'])
                trt = (move['out'] - move['in']).total_seconds() / 3600
                station = move['lane'].station
                if station.id in data:
                    data[station.id]['time'] += time
                    data[station.id]['trt'] += trt
                    data[station.id]['out'] = move['out']
                else:
                    data[station.id] = {'station': station,
                                        'time': time,
                                        'trt': trt,
                                        'in': move['in'],
                                        'out': move['out']}

        # Don't include the current station
        if self.station and self.station.id in data:
            del data[self.station.id]

        return data

    def ect(self):
        """ Returns the estimated completion time """
        if self.estimation:
            return self.estimation[max(self.estimation)]['ect']

    def pct(self):
        """ Returns the planned completion time """
        return self.plan[max(self.plan)]['ect']


class Lane(kanban.Lane):
    def __init__(self, data, board):
        super(kanban.Lane, self).__init__(data, board)
        self.station = None
        self.phase = None
        self.groups = []


class Station(kanban.Converter):
    def __init__(self, data, board):
        super().__init__(data, board)
        self.id = self.position
        self.phase = None
        self.group = None
        self.card = float(self.card)
        self.size = float(self.size)
        lanes = []
        for lane_id in self.lanes:
            lane = board.lanes[lane_id]
            assert not lane.station, "Lane {} belongs to two different stations".format(lane)
            lane.station = self
            lanes.append(lane)
        self.lanes = lanes

    def __repr__(self):
        return self.name

    def target(self, card):
        return self.size * card.size + self.card


class Phase(kanban.Converter):
    def __init__(self, data, board):
        super().__init__(data, board)
        stations = []
        for station in board.stations.values():
            if station._id in self.stations:
                assert not station.phase, "Station {} belongs to two different phases".format(station.id)
                station.phase = self
                stations.append(station)
        self.stations = stations

    def __repr__(self):
        return self.name

    def target(self, card):
        return sum([station.target(card) for station in self.stations])


class Group(kanban.Converter):
    def __init__(self, data, board):
        super().__init__(data, board)
        self.card = float(self.card)
        self.size = float(self.size)
        self._stats_ = None
        lanes = []
        for lane_id in self.lanes:
            lane = board.lanes[lane_id]
            lane.groups.append(self)
            lanes.append(lane)
        self.lanes = lanes

    def __repr__(self):
        return self.name


class Board(kanban.Board):
    def __init__(self, data, conf):
        self.lanes = {lane['Id']: Lane(lane, self) for lane in data.pop('lanes')}
        self.stations = {station['Position']: Station(station, self) for station in data.pop('stations')}
        self.phases = {phase['Position']: Phase(phase, self) for phase in data.pop('phases')}
        self.groups = {group['Name']: Group(group, self) for group in data.pop('groups')}
        self.card_types = {card_type['Id']: kanban.CardType(card_type, self) for card_type in data.pop('card_types')}
        self.classes_of_service = {class_of_service['Id']: kanban.ClassOfService(class_of_service, self) for class_of_service in data.pop('classes_of_service')}
        self.users = {user['Id']: kanban.User(user, self) for user in data.pop('users')}
        self.cards = {card['Id']: Card(card, self) for card in data.pop('cards')}
        super(kanban.Board, self).__init__(data, None)
        start = conf['OfficeHours']['Open']
        close = conf['OfficeHours']['Close']
        self.timer = officehours.Calculator(start, close, conf['Holidays'])
