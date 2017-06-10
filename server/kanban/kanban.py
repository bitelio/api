# -*- coding: utf-8 -*-

import re
from datetime import datetime
import officehours

from cached_property import cached_property
from .. import database


class Converter:
    def __init__(self, data, board):
        self.board = board
        for attr in data:
            setattr(self, self.snake_case(attr), data[attr])

    def __repr__(self):
        return str(self.id)

    @staticmethod
    def snake_case(camelcase):
        camelcase = camelcase.replace('ID', '_id')
        if len(camelcase) > 1:
            camelcase = camelcase[0].lower() + camelcase[1:]
            return re.sub('([A-Z])', lambda match: '_' + match.group(1).lower(), camelcase)
        else:
            return camelcase.lower()


class Card(Converter):
    def __init__(self, data, board):
        super().__init__(data, board)
        self.history = data['History']

    def __str__(self):
        return str(self.external_card_id or self.id)

    @property
    def lane(self):
        """ Returns the current lane """
        return self.moves[-1]['lane']

    @property
    def creation_date(self):
        for event in self.history:
            if event['Type'] == 'CardCreationEventDTO':
                return event['DateTime']

    @property
    def first_date(self):
        """ Date of the first event in the card's history """
        return self.history[0]['DateTime']

    @property
    def archived(self):
        """ Returns True if the card is in one of the archive lnaes """
        return self.lane in self.board.archive_lanes

    @cached_property
    def moves(self):
        """ Returns a list of card movements in chronological order """
        previous_time = self.creation_date or self.first_date
        current_time = None
        moves = []
        current_lane = self.board.lanes.get(self.history[0]['ToLaneId'])
        for event in self.history:
            if event['Type'] == 'CardMoveEventDTO':
                current_time = event['DateTime']
                moves.append({'lane': self.board.lanes.get(event['FromLaneId']),
                              'in': previous_time, 'out': current_time})
                previous_time = current_time
                current_lane = self.board.lanes.get(event['ToLaneId'])
        moves.append({'lane': current_lane, 'in': current_time or previous_time, 'out': None})
        return moves

    @cached_property
    def tagset(self):
        """ Returns a list of tags """
        result = []
        for event in self.history:
            if event['Type'] == 'CardFieldsChangedEventDTO':
                for change in event['Changes']:
                    if change['FieldName'] == 'Tags':
                        old_tags = change['OldValue'].split(',') if change['OldValue'] else []
                        new_tags = change['NewValue'].split(',') if change['NewValue'] else []
                        if new_tags > old_tags:
                            diff = set(new_tags) - set(old_tags)
                            result.append({'tag': ','.join(diff), 'date': event['DateTime']})
        return result

    @cached_property
    def comments(self):
        """ Returns a list of comments """
        result = []
        for event in self.history:
            if event['Type'] == 'CommentPostEventDTO':
                user = next((user for user in self.board.users.values()
                    if user.user_name == event['UserName'].lower()), None)
                comment = Comment(event['CommentText'], event['DateTime'], user)
                result.append(comment)
        return result


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


class Lane(Converter):
    def __init__(self, data, board):
        super().__init__(data, board)
        self.station = None

    def __str__(self):
        return self.path

    @property
    def ascendants(self):
        """ Returns a list of all parent lanes sorted in ascending order """
        lanes = []
        lane = self.parent
        while lane:
            lanes.append(lane)
            lane = lane.parent
        return lanes

    @property
    def descendants(self):
        """ Returns a list of all child lanes sorted in descending order """
        def sublanes(lane, array):
            for child in lane.children:
                array.append(child)
                sublanes(child, array)
            return array

        return sublanes(self, [])

    @property
    def top_lane(self):
        """ Returns the top parent lane, or itself if none """
        return ([self] + self.ascendants)[-1]

    @property
    def children(self):
        return [self.board.lanes[lane_id] for lane_id in self.child_lane_ids]

    @property
    def siblings(self):
        return [self.board.lanes.get(lane) for lane in self.sibling_lane_ids]

    @property
    def parent(self):
        return self.board.lanes.get(self.parent_lane_id)

    @property
    def path(self):
        return '::'.join(reversed([self.title] + [lane.title for lane in self.ascendants]))

    @property
    def cards(self):
        return [card for card in self.board.cards.values() if card.lane == self]


class Station(Converter):
    def __init__(self, data, board):
        super().__init__(data, board)
        # self.position = self.id
        self.id = self.position
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


class Phase(Converter):
    def __init__(self, data, board):
        self.id = self.position
        stations = []
        for station_id in self.stations:
            station = board.stations[station_id]
            assert not station.phase, "Station {} belongs to two different phases".format(station)
            station.phase = self
            stations.append(station)
        self.stations = stations

    def __repr__(self):
        return self.name


class Board(Converter):
    def __init__(self, board_id):
        data = database.load.db.boards.find_one({'Id': board_id})
        data.update(database.load.db.settings.find_one({'Id': board_id}))
        self.timer = officehours.Calculator(data['OfficeHours']['Open'], data['OfficeHours']['Close'], [])
        self.lanes = {lane['Id']: Lane(lane, self) for lane in database.load.lanes(board_id)}
        self.stations = {station['Position']: Station(station, self) for station in database.load.stations(board_id)}
        self.cards = {card['Id']: Card(card, self) for card in database.load.cards(board_id)}
        super().__init__(data, self)

    def __str__(self):
        return self.title

    @property
    def sorted_lanes(self):
        lanes = []
        lanes += self.backlog_lanes
        for lane in self.top_level_lanes:
            lanes += [lane] + lane.descendants
        lanes += self.archive_lanes
        return lanes

    @property
    def backlog_lanes(self):
        backlog = self.lanes[self.backlog_top_level_lane_id]
        return [backlog] + backlog.descendants

    @property
    def archive_lanes(self):
        archive = self.lanes[self.archive_top_level_lane_id]
        return [archive] + archive.descendants

    # @property
    # def wip_lanes(self):
        # return [lane for lane in self.lanes.values() if lane.area == 'wip']

    @property
    def top_level_lanes(self):
        return [self.lanes[lane_id] for lane_id in self.top_level_lane_ids]

