import dateutils


def selected(cards, filters):
    for attr in ['Priority']:
        filtered = []
        for card in cards:
            if card.get(attr) in filters[attr]:
                filtered.append(card)
        cards = filtered
    return cards


def applies(event):
    if event['Type'] == 'CardMoveEventDTO' \
            and from_date < event['DateTime'] < to_date \
            and board.get_station(event['FromLaneId']):
        station = board.get_station(event['FromLaneId'])
        stations[station['Id']]['TRT'] += 0

def averages(board, args):
    cards = selected(board.cards, filters)
    from_date = dateutils.parse(args['From'])
    to_date = dateutils.parse(args['To'])
    for card in cards:
        for event in card.history:
            if event['CardMoveEventDTO']:
                if from_date < event['DateTime'] < to_date:
for card in cards:
    if applies(card):  # Check card type, priority, etc.
        for move in card.moves:
            considered = False
            if from_date < move.date < to_date:
                account_move(move)  # Add TRT to station
                stations_in = []
                stations_out = []
                considered = True
                lane = move.lane
            if considered:
                station.wip(lane)
