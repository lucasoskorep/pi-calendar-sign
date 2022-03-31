from datetime import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from event import Event
from time import sleep


class CalGrab(object):

    def __init__(self, auth_file, calendars=[], callbacks=[]):
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

        :param frequency: Amount of time to wait between updates in seconds
        :param time_to_update: normally set to -1 aka no limit.  Time in minutes to continually ping the api for.
        :return: None
        """
        try:
            start = None
            while True:
                now = datetime.utcnow() # 'Z' indicates UTC time
                now_str = now.isoformat() + 'Z'
                if start ==None:
                    start = now
                print('Getting the upcoming 10 events')
                events_result = self.service.events().list(calendarId='loskorep@productiveedge.com', timeMin=now_str,
                                                      maxResults=10, singleEvents=True,
                                                      orderBy='startTime').execute()
                events = events_result.get('items', [])

                if not events:
                    print('No upcoming events found.')
                    return

                events = [Event.get_from_gcal_api_json(json) for json in events]
                for callback in self.callbacks:
                    callback(events)
                if (now-start).total_seconds() > time_to_update:
                    return
                sleep(frequency)
        except HttpError as error:
            print('An error occurred: %s' % error)
