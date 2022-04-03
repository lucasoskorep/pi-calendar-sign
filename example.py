from calendar_grabber import CalGrab


def process_events(events):
    print("PROCESSING EVENTS")
    for event in events:
        print(event)


def main():
    cg = CalGrab("./.auth.json", "loskorep@productiveedge.com", [process_events])
    cg.update_at_interval(5, 15)


if __name__ == '__main__':
    main()
