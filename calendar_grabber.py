from datetime import datetime
from time import sleep

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from event import Event


class CalGrab(object):

    def __init__(self, auth_file, calendars=None, callbacks=None):
        if callbacks is None:
            callbacks = []
        if calendars is None:
            calendars = []
        self.calendars = calendars
        self.callbacks = callbacks
        self.creds = service_account.Credentials.from_service_account_file(
            auth_file, scopes=['https://www.googleapis.com/auth/calendar.readonly'])
        try:
            self.service = build('calendar', 'v3', credentials=self.creds)
        except HttpError as error:
            raise error

    def update_at_interval(self, frequency, time_to_update=-1):
        """

        :param frequency:
        :param time_to_update:
        :return:
        """
        start = None
        while True:
            try:
                now = datetime.utcnow()
                if start == None:
                    start = now
                all_events = []
                for calendar in self.calendars:
                    print("processing calendar")
                    events_result = self.service.events().list(
                        calendarId=calendar,
                        timeMin=now.isoformat() + 'Z',
                        maxResults=10,
                        singleEvents=True,
                        orderBy='startTime'
                    ).execute()
                    events = events_result.get('items', [])
                    if not events:
                        print('No upcoming events found.')
                        return
                    all_events.extend([i for i in [Event.get_from_gcal_api_json(json) for json in events] if i is not None])
                print(all_events)
                all_events = sorted(all_events, key=lambda event: event.start_time)
                for callback in self.callbacks:
                    callback(all_events)
                if time_to_update > 0 and (now - start).total_seconds() > time_to_update:
                    return
                sleep(frequency)
            except HttpError as error:
                print('An error occurred: %s' % error)
