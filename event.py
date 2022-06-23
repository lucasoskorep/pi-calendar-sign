from dateutil.parser import parse


class Event(object):

    def __init__(self, summary, start_time, end_time):
        self.summary = summary
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return f"summary : {self.summary}, end_time : {self.end_time}, start_time : {self.start_time}"

    @staticmethod
    def get_from_gcal_api_json(json):
        try:
            print(json['start'].get('dateTime'))
            return Event(
                json['summary'] if 'summary' in json else "No Title",
                parse(json['start'].get('dateTime')),
                parse(json['end'].get('dateTime'))
            )
        except Exception as e:
            print(e)
            return None
