import os.path
from google.auth.transport.requests import Request
from google.auth.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.message import EmailMessage
from typing import Dict
import base64
from datetime import datetime, timezone
from typing import Dict

SCOPES = [
    "https://www.googleapis.com/auth/gmail",
    "https://www.googleapis.com/auth/calendar",
]


def read_email():
    creds = authenticate_gmail()
    service = build("gmail", "v1", credentials=creds)
    response = (
        service.users()
        .messages()
        .list(userId="me", q="label:important is:unread")
        .execute()
    )
    return response


def check_schedules():
    creds = authenticate_gmail()
    service = build("calendar", "v3", credentials=creds)

    now = datetime.now(tz=timezone.utc).isoformat()
    event_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = event_result.get("items", [])
    if not events:
        return "No meetings"

    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        return {"start": start, "event_summary": event["summary"]}


def schedule_meeting(request_body: Dict):
    creds = authenticate_gmail()
    service = build("calendar", "v3", credentials=creds)

    event = service.events().insert(calendarId="primary", body=request_body).execute()
    return event.get("htmlLink")


def send_email(data: Dict):
    creds = authenticate_gmail()
    service = build("gmail", "v1", credentials=creds)

    message = EmailMessage()
    message.set_content(data.get("content"))

    message["To"] = data.get("to")
    message["From"] = data.get("from")
    message["Subject"] = data.get("subject")

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {"raw": encoded_message}

    response = (
        service.users().messages().send(userId="me", body=create_message).execute()
    )

    return response


def authenticate_gmail():
    try:
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return creds
    except HttpError as e:
        print(e)
