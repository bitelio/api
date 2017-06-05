from dateutil.parser import parse

from .. import kanban


attrs = {'Priority': 'priority', 'TypeId': 'type_id'}

def selected(cards, filters):
    for attr in ['Priority', 'TypeId']:
        if attr not in filters:
            continue
        filtered = []
        for card in cards:
            if getattr(card, attrs[attr]) in filters[attr]:
                filtered.append(card)
        cards = filtered
    return cards


# def applies(event):
    # if event['Type'] == 'CardMoveEventDTO' \
            # and from_date < event['DateTime'] < to_date \
            # and board.get_station(event['FromLaneId']):
        # station = board.get_station(event['FromLaneId'])
        # stations[station['Id']]['TRT'] += 0


# def averages(board, args):
    # cards = selected(board.cards, filters)
    # from_date = dateutils.parse(args['From'])
    # to_date = dateutils.parse(args['To'])
    # for card in cards:
        # for event in card.history:
            # if event['CardMoveEventDTO']:
                # if from_date < event['DateTime'] < to_date:
                    # pass

def averages(board_id, args):
    board = kanban.load(board_id)
    if args:
        cards = selected(board.cards.values(), args)
    else:
        cards = list(board.cards.values())
    print(args.get('FromDate'), args.get('ToDate'))
    from_date = parse(args['FromDate']) if args['FromDate'] else None
    to_date = parse(args['ToDate']) if args['ToDate'] else None
    print(from_date, to_date)
    stations = {}
    columns = ['position', 'name', 'cards in', 'cards out', 'cards wip', 'sheets in', 'sheets out',
               'sheets wip', 'avg trt card', 'avg trt sheet', 'diff', 'card', 'sheet']
    for station in board.stations.values():
        stations[station] = {'name': station.name, 'card': station.card, 'sheet': station.size}
        stations[station]['position'] = station.position
        for col in columns[2:8] + ['trt']:
            stations[station][col] = 0

    for card in cards:
        if hasattr(card.lane, 'station') and card.lane.station:
            stations[card.lane.station]['cards wip'] += 1
            stations[card.lane.station]['sheets wip'] += card.size
        for station in card.stations:
            if station:
                if from_date and card.stations[station]['out'] < from_date:
                    continue
                if to_date and card.stations[station]['out'] > to_date:
                    continue
                stations[station]['cards out'] += 1
                stations[station]['sheets out'] += card.size
                stations[station]['trt'] += card.stations[station]['trt']

    for station in stations.values():
        station['cards in'] = station['cards out'] + station['cards wip']
        station['sheets in'] = station['sheets out'] + station['sheets wip']
        if station['cards out'] > 0:
            station['avg trt card'] = station['trt'] / station['cards out']
        else:
            station['avg trt card'] = 'N/A'
        if station['sheets out'] > 0:
            station['avg trt sheet'] = station['trt'] / station['sheets out']
            station['diff'] = station['avg trt sheet'] - station['card'] + station['sheet']
        else:
            station['avg trt sheet'] = 'N/A'
            station['diff'] = 'N/A'

    table = []
    for item in stations.values():
        row = []
        for col in columns:
            if isinstance(item[col], str):
                row.append(item[col])
            else:
                row.append(round(item[col], 2))
        table.append(row)

    return {'data': table}


# for card in cards:
    # if applies(card):  # Check card type, priority, etc.
        # for move in card.moves:
            # considered = False
            # if from_date < move.date < to_date:
                # account_move(move)  # Add TRT to station
                # stations_in = []
                # stations_out = []
                # considered = True
                # lane = move.lane
            # if considered:
                # station.wip(lane)
