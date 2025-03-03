from ..integrations import read_email, format_read_email_response_for_tts
from typing import Dict, Optional

"""
Routes a given intent to its corresponding action.

Parameters:
    intent (str): The intent to be routed, such as "read_emails", "send_email", or "set_reminders".

Returns:
    str: A string representing the action associated with the intent.
"""


def route_request(intent: str, data: Optional[Dict] = None):
    match (intent):
        case "read_emails":
            gmail_response = read_email()
            formatted_response_for_tts = format_read_email_response_for_tts(
                gmail_response
            )
            return formatted_response_for_tts
        case "send_email":
            nlp_response = ""
            gmail_response = ""
            formatted_response_for_tts = ""
            return "Send"
        case "set_reminders":
            return "Set Reminders"
