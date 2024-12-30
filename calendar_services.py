import datetime

from googleapiclient.errors import HttpError


def get_all_calendar_names(service):
    # Getting list of Calendar ids
    page_token = None
    try:
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                print(
                    f"{calendar_list_entry['summary']}")
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
    except HttpError as error:
        print(f"An error occurred: {error}")


def get_calendar_id_by_name(service, name) -> str:
    # Getting list of Calendar ids
    page_token = None
    try:
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                if (calendar_list_entry['summary'] == name):
                    return calendar_list_entry['id']
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                print(f"Warning: cannot retrieve calendar id of name '{name}'")
                return "None"
    except HttpError as error:
        print(f"An error occurred: {error}")


def get_all_calendar_ids(service):
    # Getting list of Calendar ids
    page_token = None
    try:
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                print(
                    f"{calendar_list_entry['summary']} id: {calendar_list_entry['id']}")
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
    except HttpError as error:
        print(f"An error occurred: {error}")


def get_next_n_events_of_calendar(service, n=10, id="primary"):
    try:
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        events_result = (
            service.events()
            .list(
                calendarId=id,
                timeMin=now,
                maxResults=n,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])
    except HttpError as error:
        print(f"An error occurred: {error}")


def create_calendar(service, calendarName):
    calendar = {
        'summary': f'{calendarName}',
        'timeZone': 'America/Chicago'
    }

    created_calendar = service.calendars().insert(body=calendar).execute()
    # print(created_calendar['id'])


"""
Creates an event object given processed user input

    Parameters:
        summary (str): Title of the event, e.g. "Charlie Brown's appt"
        email (str): email of the attendee, e.g. 'c-brown@gmail.com'
        start (str): The start datetime in standard ISO 8601 e.g. "YY-MM-DDT13:00:00Z"
        end (str): The end date/datetime in standard ISO 8601
        description (str, optional): Brief description of the event 
        location (str, optional): Location of the event
    
    Return:
        event (Object)
"""


def create_an_event(summary, email, start, end, description='', location='', recurrence=[]):
    return {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start,  # '2024-12-31T10:30:00',
            'timeZone': 'America/Chicago',
        },
        'end': {
            'dateTime': end,  # '2024-12-31T13:00:00',
            'timeZone': 'America/Chicago',
        },
        'attendees':  [{'email': email}],
        'recurrence': recurrence
    }


def add_event_to_calendar(service, event, calendarID="primary"):
    try:
        service.events().insert(calendarId=calendarID, body=event).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")
