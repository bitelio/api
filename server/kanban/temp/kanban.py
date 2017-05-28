# -*- coding: utf-8 -*-

import re

from cached_property import cached_property


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
        self.type = board.card_types[self.type_id]
        self.assigned_user = board.users.get(data['AssignedUserId'])
        self.class_of_service = board.classes_of_service.get(data['ClassOfServiceId'])
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


class Lane(Converter):
    def __init__(self, data, board):
        super().__init__(data, board)

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


class Board(Converter):
    def __init__(self, data):
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

