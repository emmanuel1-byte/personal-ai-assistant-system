from ..integrations import (
    read_email,
    send_email,
    schedule_meeting,
    check_schedules,
    format_schedule_response_for_tts,
    format_read_email_response_for_tts,
    generate_email_send_confirmation_message_for_tts,
    format_send_email_for_gmail,
    format_create_schedule_request,
)
from typing import Dict, Optional


"""
Routes requests based on the specified intent and processes them accordingly.

Parameters:
    intent (str): The intent of the request, determining the action to perform.
    stt_response (Optional[str]): The speech-to-text response, used for scheduling meetings.
    data (Optional[Dict]): Additional data required for certain intents, such as email details.

Returns:
    str: A formatted response suitable for text-to-speech output or a calendar event link.

The function supports the following intents:
- "read_emails": Reads unread emails and formats the response for TTS.
- "send_email": Sends an email and generates a confirmation message for TTS.
- "check_schedules": Checks the user's schedule and formats the response for TTS.
- "schedule_meeting": Schedules a meeting and returns the event link.
"""


def route_request(
    intent: str, data: Optional[Dict] = None
):
    match (intent):
        case "read_emails":
            gmail_response = read_email()
            formatted_response_for_tts = format_read_email_response_for_tts(
                gmail_response
            )
            return formatted_response_for_tts
        case "send_email":
            formatted_response_for_email_sending = format_send_email_for_gmail(
                type=data.get("type"),
                recipient=data.get("email"),
                content=data.get("content"),
            )
            gmail_response = send_email(formatted_response_for_email_sending)
            response_for_tts = generate_email_send_confirmation_message_for_tts()
            return response_for_tts
        case "check_schedules":
            gmail_response = check_schedules()
            response_for_tts = format_schedule_response_for_tts(gmail_response)
            return response_for_tts
        # case "schedule_meeting":
            # formatted_response_for_calender_event = format_create_schedule_request(
            #     stt_response
            # )
            # calender_response = schedule_meeting(formatted_response_for_calender_event)
            # return calender_response
