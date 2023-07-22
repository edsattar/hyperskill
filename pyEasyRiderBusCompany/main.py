from datetime import datetime
import re

data1_1: list[dict] = [
    {"bus_id": 128,   "stop_id": 1,   "stop_name": "Prospekt Avenue",  "next_stop": 3,   "stop_type": "S", "a_time": 8.12},
    {"bus_id": 128,   "stop_id": 3,   "stop_name": "",                 "next_stop": 5,   "stop_type": "",  "a_time": "08:19"},
    {"bus_id": 128,   "stop_id": 5,   "stop_name": "Fifth Avenue",     "next_stop": 7,   "stop_type": "O", "a_time": "08:25"},
    {"bus_id": 128,   "stop_id": "7", "stop_name": "Sesame Street",    "next_stop": 0,   "stop_type": "F", "a_time": "08:37"},
    {"bus_id": "",    "stop_id": 2,   "stop_name": "Pilotow Street",   "next_stop": 3,   "stop_type": "S", "a_time": ""},
    {"bus_id": 256,   "stop_id": 3,   "stop_name": "Elm Street",       "next_stop": 6,   "stop_type": "",  "a_time": "09:45"},
    {"bus_id": 256,   "stop_id": 6,   "stop_name": "Sunset Boulevard", "next_stop": 7,   "stop_type": "",  "a_time": "09:59"},
    {"bus_id": 256,   "stop_id": 7,   "stop_name": "Sesame Street",    "next_stop": "0", "stop_type": "F", "a_time": "10:12"},
    {"bus_id": 512,   "stop_id": 4,   "stop_name": "Bourbon Street",   "next_stop": 6,   "stop_type": "S", "a_time": "08:13"},
    {"bus_id": "512", "stop_id": 6,   "stop_name": "Sunset Boulevard", "next_stop": 0,   "stop_type": 5,   "a_time": "08:16"}]
data1_3: list[dict] = [
    {"bus_id": 128,      "stop_id": 1,      "stop_name": "Fifth Avenue",            "next_stop": 4,     "stop_type": "S", "a_time": "08:12"},
    {"bus_id": 128,      "stop_id": 4,      "stop_name": "abbey Road",              "next_stop": 5,     "stop_type": "",  "a_time": "08:19"},
    {"bus_id": 128,      "stop_id": 5,      "stop_name": "Santa Monica Boulevard",  "next_stop": 8,     "stop_type": "O", "a_time": "08:25"},
    {"bus_id": 128,      "stop_id": 8,      "stop_name": "Elm Street Str.",         "next_stop": "11",  "stop_type": "",  "a_time": "08:37"},
    {"bus_id": 128,      "stop_id": 11,     "stop_name": "Beale Street",            "next_stop": 12,    "stop_type": "",  "a_time": "09:20"},
    {"bus_id": 128,      "stop_id": 12,     "stop_name": 9,                         "next_stop": 14,    "stop_type": "",  "a_time": "09:45"},
    {"bus_id": 128,      "stop_id": "five", "stop_name": "Bourbon street",          "next_stop": 19,    "stop_type": "O", "a_time": "09:59"},
    {"bus_id": 128,      "stop_id": 19,     "stop_name": "",                        "next_stop": 0,     "stop_type": "F", "a_time": "10:12"},
    {"bus_id": 256,      "stop_id": 2,      "stop_name": "Pilotow Street",          "next_stop": 3,     "stop_type": "S", "a_time": "08:13"},
    {"bus_id": "",       "stop_id": "",     "stop_name": "Startowa Street",         "next_stop": 8,     "stop_type": 23.9, "a_time": 8},
    {"bus_id": 256,      "stop_id": 8,      "stop_name": "Elm",                     "next_stop": 10,    "stop_type": "",  "a_time": "08:29"},
    {"bus_id": 256,      "stop_id": 10,     "stop_name": "Lombard Street",          "next_stop": 12,    "stop_type": "",  "a_time": "08:44"},
    {"bus_id": 256,      "stop_id": 12,     "stop_name": "Sesame Street",           "next_stop": "",    "stop_type": "O", "a_time": "08:46"},
    {"bus_id": 256,      "stop_id": 13,     "stop_name": 34.6,                      "next_stop": 16,    "stop_type": "",  "a_time": "09:13"},
    {"bus_id": "eleven", "stop_id": 16,     "stop_name": "Sunset Boullevard",       "next_stop": 17.4,  "stop_type": "O", "a_time": "09:26"},
    {"bus_id": 256,      "stop_id": 17,     "stop_name": "Khao San Road",           "next_stop": 20,    "stop_type": "O", "a_time": "10:25"},
    {"bus_id": 256,      "stop_id": 20,     "stop_name": "Michigan Avenue",         "next_stop": 0,     "stop_type": "F", "a_time": "11:26"},
    {"bus_id": 512,      "stop_id": 6,      "stop_name": "Arlington Road",          "next_stop": 7,     "stop_type": "S", "a_time": "11:06"},
    {"bus_id": 512,      "stop_id": 7,      "stop_name": "Parizska St.",            "next_stop": 8,     "stop_type": "",  "a_time": "11:15"},
    {"bus_id": 512,      "stop_id": 8,      "stop_name": "Elm Street",              "next_stop": 9,     "stop_type": "",  "a_time": "11:56"},
    {"bus_id": 512,      "stop_id": 9,      "stop_name": "Niebajka Av.",            "next_stop": 15,    "stop_type": "",  "a_time": "12:20"},
    {"bus_id": 512,      "stop_id": 15,     "stop_name": "Jakis Street",            "next_stop": 16,    "stop_type": "",  "a_time": "12:44"},
    {"bus_id": 512,      "stop_id": 16,     "stop_name": "Sunset Boulevard",        "next_stop": 18,    "stop_type": "",  "a_time": "13:01"},
    {"bus_id": 512,      "stop_id": 18,     "stop_name": "Jakas Avenue",            "next_stop": 19,    "stop_type": 3,   "a_time": "14:00"},
    {"bus_id": 1024,     "stop_id": "21",   "stop_name": "Karlikowska Avenue",      "next_stop": 12,    "stop_type": "S", "a_time": 13.01},
    {"bus_id": 1024,     "stop_id": 12,     "stop_name": "Sesame Street",           "next_stop": 0,     "stop_type": "FF", "a_time": ""},
    {"bus_id": "",       "stop_id": 19,     "stop_name": "Prospekt Avenue",         "next_stop": 0,     "stop_type": "F", "a_time": "14:11"}]
data2_1: list[dict] = [
    {"bus_id": 128, "stop_id": 1, "stop_name": "Prospekt Avenue", "next_stop": 3, "stop_type": "S", "a_time": "08:12"},
    {"bus_id": 128, "stop_id": 3, "stop_name": "Elm Street", "next_stop": 5, "stop_type": "", "a_time": "08:19"},
    {"bus_id": 128, "stop_id": 5, "stop_name": "Fifth Avenue", "next_stop": 7, "stop_type": "O", "a_time": "08:25"},
    {"bus_id": 128, "stop_id": 7, "stop_name": "Sesame Street", "next_stop": 0, "stop_type": "F", "a_time": "08:37"},
    {"bus_id": 256, "stop_id": 2, "stop_name": "Pilotow Street", "next_stop": 3, "stop_type": "S", "a_time": "09:20"},
    {"bus_id": 256, "stop_id": 3, "stop_name": "Elm Street", "next_stop": 6, "stop_type": "", "a_time": "09:45"},
    {"bus_id": 256, "stop_id": 6, "stop_name": "Sunset Boulevard", "next_stop": 7, "stop_type": "", "a_time": "09:59"},
    {"bus_id": 256, "stop_id": 7, "stop_name": "Sesame Street", "next_stop": 0, "stop_type": "F", "a_time": "10:12"},
    {"bus_id": 512, "stop_id": 4, "stop_name": "Bourbon Street", "next_stop": 6, "stop_type": "S", "a_time": "08:13"},
    {"bus_id": 512, "stop_id": 6, "stop_name": "Sunset Boulevard", "next_stop": 0, "stop_type": "F", "a_time": "08:16"}]
data4_1: list[dict] = [
    {"bus_id": 128, "stop_id": 1, "stop_name": "Prospekt Avenue",  "next_stop": 3, "stop_type": "S", "a_time": "08:12"},
    {"bus_id": 128, "stop_id": 3, "stop_name": "Elm Street",       "next_stop": 5, "stop_type": "",  "a_time": "08:19"},
    {"bus_id": 128, "stop_id": 5, "stop_name": "Fifth Avenue",     "next_stop": 7, "stop_type": "O", "a_time": "08:25"},
    {"bus_id": 128, "stop_id": 7, "stop_name": "Sesame Street",    "next_stop": 0, "stop_type": "F", "a_time": "08:37"},
    {"bus_id": 512, "stop_id": 4, "stop_name": "Bourbon Street",   "next_stop": 6, "stop_type": "",  "a_time": "08:13"},
    {"bus_id": 512, "stop_id": 6, "stop_name": "Sunset Boulevard", "next_stop": 0, "stop_type": "F", "a_time": "08:16"}]
data4_2: list[dict] = [
    {"bus_id": 129, "stop_id": 1, "stop_name": "Prospekt Avenue",  "next_stop": 3, "stop_type": "S", "a_time": "08:12"},
    {"bus_id": 128, "stop_id": 3, "stop_name": "Elm Street",       "next_stop": 5, "stop_type": "",  "a_time": "08:19"},
    {"bus_id": 128, "stop_id": 5, "stop_name": "Fifth Avenue",     "next_stop": 7, "stop_type": "O", "a_time": "08:25"},
    {"bus_id": 128, "stop_id": 7, "stop_name": "Sesame Street",    "next_stop": 0, "stop_type": "",  "a_time": "08:37"},
    {"bus_id": 512, "stop_id": 4, "stop_name": "Bourbon Street",   "next_stop": 6, "stop_type": "S", "a_time": "08:13"},
    {"bus_id": 512, "stop_id": 6, "stop_name": "Sunset Boulevard", "next_stop": 0, "stop_type": "F", "a_time": "08:16"},]
data4_3: list[dict] = [
    {"bus_id": 128, "stop_id": 1, "stop_name": "Prospekt Avenue",  "next_stop": 3, "stop_type": "S", "a_time": "08:12"},
    {"bus_id": 128, "stop_id": 3, "stop_name": "Elm Street",       "next_stop": 5, "stop_type": "",  "a_time": "08:19"},
    {"bus_id": 128, "stop_id": 5, "stop_name": "Fifth Avenue",     "next_stop": 7, "stop_type": "O", "a_time": "08:25"},
    {"bus_id": 128, "stop_id": 7, "stop_name": "Sesame Street",    "next_stop": 0, "stop_type": "F", "a_time": "08:37"},
    {"bus_id": 256, "stop_id": 2, "stop_name": "Pilotow Street",   "next_stop": 3, "stop_type": "S", "a_time": "09:20"},
    {"bus_id": 256, "stop_id": 3, "stop_name": "Elm Street",       "next_stop": 6, "stop_type": "",  "a_time": "09:45"},
    {"bus_id": 256, "stop_id": 6, "stop_name": "Sunset Boulevard", "next_stop": 7, "stop_type": "",  "a_time": "09:59"},
    {"bus_id": 256, "stop_id": 7, "stop_name": "Sesame Street",    "next_stop": 0, "stop_type": "F", "a_time": "10:12"},
    {"bus_id": 512, "stop_id": 4, "stop_name": "Bourbon Street",   "next_stop": 6, "stop_type": "S", "a_time": "08:13"},
    {"bus_id": 512, "stop_id": 6, "stop_name": "Sunset Boulevard", "next_stop": 0, "stop_type": "F", "a_time": "08:16"}]
data5_1: list[dict] = [
    {"bus_id": 128, "stop_id": 1, "stop_name": "Prospekt Avenue",  "next_stop": 3, "stop_type": "S", "a_time": "08:12"},
    {"bus_id": 128, "stop_id": 3, "stop_name": "Elm Street",       "next_stop": 5, "stop_type": "",  "a_time": "08:19"},
    {"bus_id": 128, "stop_id": 5, "stop_name": "Fifth Avenue",     "next_stop": 7, "stop_type": "O", "a_time": "08:17"},
    {"bus_id": 128, "stop_id": 7, "stop_name": "Sesame Street",    "next_stop": 0, "stop_type": "F", "a_time": "08:07"},
    {"bus_id": 256, "stop_id": 2, "stop_name": "Pilotow Street",   "next_stop": 3, "stop_type": "S", "a_time": "09:20"},
    {"bus_id": 256, "stop_id": 3, "stop_name": "Elm Street",       "next_stop": 6, "stop_type": "",  "a_time": "09:45"},
    {"bus_id": 256, "stop_id": 6, "stop_name": "Sunset Boulevard", "next_stop": 7, "stop_type": "",  "a_time": "09:44"},
    {"bus_id": 256, "stop_id": 7, "stop_name": "Sesame Street",    "next_stop": 0, "stop_type": "F", "a_time": "10:12"},
    {"bus_id": 512, "stop_id": 4, "stop_name": "Bourbon Street",   "next_stop": 6, "stop_type": "S", "a_time": "08:13"},
    {"bus_id": 512, "stop_id": 6, "stop_name": "Sunset Boulevard", "next_stop": 0, "stop_type": "F", "a_time": "08:16"}]
data5_2: list[dict] = [
    {"bus_id": 512, "stop_id": 4, "stop_name": "Bourbon Street",   "next_stop": 6, "stop_type": "S", "a_time": "08:13"},
    {"bus_id": 512, "stop_id": 6, "stop_name": "Sunset Boulevard", "next_stop": 0, "stop_type": "F", "a_time": "08:16"}]
data6_1: list[dict] = [
    {"bus_id": 128, "stop_id": 1, "stop_name": "Prospekt Avenue",  "next_stop": 3, "stop_type": "S", "a_time": "08:12"},
    {"bus_id": 128, "stop_id": 3, "stop_name": "Elm Street",       "next_stop": 5, "stop_type": "O", "a_time": "08:19"},
    {"bus_id": 128, "stop_id": 5, "stop_name": "Fifth Avenue",     "next_stop": 7, "stop_type": "O", "a_time": "08:25"},
    {"bus_id": 128, "stop_id": 7, "stop_name": "Sesame Street",    "next_stop": 0, "stop_type": "F", "a_time": "08:37"},
    {"bus_id": 256, "stop_id": 2, "stop_name": "Pilotow Street",   "next_stop": 3, "stop_type": "S", "a_time": "09:20"},
    {"bus_id": 256, "stop_id": 3, "stop_name": "Elm Street",       "next_stop": 6, "stop_type": "",  "a_time": "09:45"},
    {"bus_id": 256, "stop_id": 6, "stop_name": "Sunset Boulevard", "next_stop": 7, "stop_type": "O", "a_time": "09:59"},
    {"bus_id": 256, "stop_id": 7, "stop_name": "Sesame Street",    "next_stop": 0, "stop_type": "F", "a_time": "10:12"},
    {"bus_id": 512, "stop_id": 4, "stop_name": "Bourbon Street",   "next_stop": 6, "stop_type": "S", "a_time": "08:13"},
    {"bus_id": 512, "stop_id": 6, "stop_name": "Sunset Boulevard", "next_stop": 0, "stop_type": "F", "a_time": "08:16"}]


def is_valid_stop_type(stop_type):
    pattern = r"^[SOF]?$"
    return type(stop_type) is str and re.match(pattern, stop_type)


def is_valid_a_time(time_str):
    pattern = r"([01][0-9]|2[0-3]):[0-5][0-9]$"
    return type(time_str) is str and re.match(pattern, time_str)


def is_valid_stop_name(stop_name):
    pattern = r"([A-Z][a-z]+ )+(Road|Avenue|Boulevard|Street)$"
    return type(stop_name) is str and re.match(pattern, stop_name)


def stage1() -> None:
    errors: dict[str, int] = {
        "bus_id": 0,
        "stop_id": 0,
        "stop_name": 0,
        "next_stop": 0,
        "stop_type": 0,
        "a_time": 0,
        "total": 0
    }

    for e in data1_1:
        if type(e["bus_id"]) is not int:
            errors["bus_id"] += 1
            errors["total"] += 1

        if type(e["stop_id"]) is not int:
            errors["stop_id"] += 1
            errors["total"] += 1

        if type(e["stop_name"]) is not str or e["stop_name"] == "":
            errors["stop_name"] += 1
            errors["total"] += 1

        if type(e["next_stop"]) is not int:
            errors["next_stop"] += 1
            errors["total"] += 1

        if not is_valid_stop_type(e["stop_type"]):
            errors["stop_type"] += 1
            errors["total"] += 1

        if type(e["a_time"]) is not str or e["a_time"] == "":
            errors["a_time"] += 1
            errors["total"] += 1

    print(f"Type and required field validation: {errors['total']}")
    print(f"errors\nbus_id: {errors['bus_id']}")
    print(f"stop_id: {errors['stop_id']}")
    print(f"stop_name: {errors['stop_name']}")
    print(f"next_stop: {errors['next_stop']}")
    print(f"stop_type: {errors['stop_type']}")
    print(f"a_time: {errors['a_time']}")


def stage2() -> None:
    errors: dict[str, int] = {
        "stop_name": 0,
        "stop_type": 0,
        "a_time": 0,
        "total": 0
    }

    for e in data1_1:
        if not is_valid_stop_name(e["stop_name"]):
            errors["stop_name"] += 1
            errors["total"] += 1

        if not is_valid_stop_type(e["stop_type"]):
            errors["stop_type"] += 1
            errors["total"] += 1

        if not is_valid_a_time(e["a_time"]):
            errors["a_time"] += 1
            errors["total"] += 1

    print(f"Format validation: {errors['total']} errors")
    print(f"stop_name: {errors['stop_name']}")
    print(f"stop_type: {errors['stop_type']}")
    print(f"a_time: {errors['a_time']}")


def stage3() -> None:
    bus_ids: dict[int, int] = {}

    for e in data2_1:
        if e["bus_id"] in bus_ids:
            bus_ids[e["bus_id"]] += 1
        else:
            bus_ids[e["bus_id"]] = 1

    print("Line names and number of stops:")
    for id, count in bus_ids.items():
        print(f"bus_id: {id}, stops: {count}")


def stage4() -> None:
    stops: dict[str, set[str]] = {
        "Start stops": set(),
        "Transfer stops": set(),
        "Finish stops": set()
    }
    tracker: set[int] = set()
    all_stops: set[str] = set()

    for e in data4_2:
        id = e["bus_id"]

        # A transfer stop is a stop shared by at least two bus lines
        if e["stop_name"] not in all_stops:
            all_stops.add(e["stop_name"])
        else:
            stops["Transfer stops"].add(e["stop_name"])

        if e["stop_type"] == 'S':
            stops["Start stops"].add(e["stop_name"])
            if id in tracker:
                break
            else:
                tracker.add(id)
        elif e["stop_type"] == 'F':
            stops["Finish stops"].add(e["stop_name"])
            if id in tracker:
                tracker.remove(id)
            else:
                break
        else:
            if id not in tracker:
                tracker.add(id)
                break

    if tracker:
        print(f"There is no start or end stop for the line: {tracker.pop()}")
    else:
        for key, val in stops.items():
            print(f"{key}: {len(val)} {sorted(val)}")


def stage5() -> None:
    visited_bus: set[int] = set()
    error_dict: dict[int, str] = {}
    prev_time: int = 0
    for e in data4_3:
        a_time = int(e["a_time"].replace(':', ''))
        if e["bus_id"] not in visited_bus:
            prev_time = a_time
            visited_bus.add(e["bus_id"])
            continue
        elif a_time <= prev_time and e["bus_id"] not in error_dict:
            error_dict[e["bus_id"]] = e["stop_name"]

        prev_time = a_time

    print("Arrival time test")
    if len(error_dict) > 0:
        for bus_id, station_name in error_dict.items():
            print(f"bus_id line {bus_id}: wrong time on station {station_name}")
    else:
        print("OK")


def stage6() -> None:
    stops: dict[str, set] = {
        'S': set(),
        'F': set(),
        'O': set(),
        '': set(),
    }
    for e in data5_1:
        stops[e["stop_type"]].add(e["stop_name"])

    issue_stops = stops['O'] & stops['S'] | stops['O'] & stops['F'] | stops['O'] & stops['']

    print("On demand stops test:")
    if issue_stops:
        print("Wrong stop type:", sorted(issue_stops))
    else:
        print("OK")


if __name__ == "__main__":
    stage6()
