from os import path, listdir
from json import load
from pytz import timezone
from datetime import datetime


def read(collection):
    with open(path.join(folder, f"{collection}.json")) as json:
        data = load(json)
    if collection is "events":
        with open(path.join(folder, "settings.json")) as json:
            settings = load(json)
        timezones = {doc["Id"]: timezone(doc["Timezone"]) for doc in settings}
        for event in data:
            date = datetime.strptime(event["DateTime"], "%Y-%m-%d %H:%M:%S")
            event["DateTime"] = timezones[event["BoardId"]].localize(date)
    return data


folder = path.join(path.dirname(__file__), "data")
collections = [path.basename(filename)[:-5] for filename in listdir(folder)]
