from datetime import datetime, time

from pytz import timezone

from calendar_grabber import CalGrab

TIMEZONE = timezone('US/Eastern')
WORK_START = time(9, 00)
WORK_STOP = time(17, 00)


def is_event_active(events, now):
    for event in events:
        if event.start_time < now and event.end_time > now:
            print("EVENT IS ACTIVE")


def is_work_time(now):
    return now < WORK_STOP and now > WORK_START


def process_events(events):
    now = datetime.now(tz=TIMEZONE)
    print("PROCESSING EVENTS")
    is_working_time = is_work_time(now.time())
    print(is_working_time)
    if is_event_active(events, now):
        if is_working_time:
            print("Meeting in Progress")
        else:
            print("Fuck me -_-")
    else:
        if is_working_time:
            print("Work time - No event")
        else:
            print("Looks like 420 to me ayooo")


def main():
    cg = CalGrab("./.auth.json", "loskorep@productiveedge.com", [process_events])
    cg.update_at_interval(5, 15)


if __name__ == '__main__':
    main()
