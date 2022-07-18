import json

from calendar_grabber import CalGrab


def process_events(events):
    print("PROCESSING EVENTS")
    for event in events:
        print(event)


def main():
    with open("config.json") as f:
        CALENDARS = json.load(f)
        print(CALENDARS)
    cg = CalGrab("./.auth.json", CALENDARS, [process_events])
    cg.update_at_interval(5, 15)


if __name__ == '__main__':
    main()
