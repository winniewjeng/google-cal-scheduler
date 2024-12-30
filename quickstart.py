import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from calendar_services import *

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
    except HttpError as error:
        print(f"An error occurred: {error}")

    # call some of the services
    # get_all_calendar_names(service)
    open_hours_calendar = get_calendar_id_by_name(
        service, "Open to Work Hours")
    if (open_hours_calendar == "None"):
        # create Open to Work Hours calendar
        print("Creating Open to Work Hours calendar...")
        create_calendar(service, "Open to Work Hours")
        open_hours_calendar = get_calendar_id_by_name(
            service, "Open to Work Hours")

    client_scheduled_calendar = get_calendar_id_by_name(
        service, "Client Scheduled")
    if (client_scheduled_calendar == "None"):
        # create Client Scheduled calendar
        print("Creating Client Scheduled calendar...")
        create_calendar(service, "Client Scheduled")
        open_hours_calendar = get_calendar_id_by_name(
            service, "Client Scheduled")

    # print(f"Open to Work Hours calendar:\n{open_hours_calendar}")
    # print(f"Client Scheduled calendar:\n{client_scheduled_calendar}")

    # client_event = create_an_event(summary="Charlie Brown's appt", email="c-brown02@mail.com", start="2024-12-31T11:30:00",
    #                                end="2024-12-31T12:30:00", description='career counselling', location='your office')
    # add_event_to_calendar(service, client_event, client_scheduled_calendar)
    work_event = create_an_event(summary="Open to work", email="c-brown02@mail.com", start="2024-12-29T11:30:00",
                                 end="2024-12-29T12:30:00", recurrence=['RRULE:FREQ=DAILY;COUNT=6', 'EXDATE;TZID=America/Chicago:20250102T113000', 'EXDATE;TZID=America/Chicago:20241231T113000'])
    add_event_to_calendar(service, work_event, open_hours_calendar)


if __name__ == "__main__":
    main()
