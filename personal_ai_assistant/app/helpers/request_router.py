"""
Routes a given intent to its corresponding action.

Parameters:
    intent (str): The intent to be routed, such as "read_emails", "send_email", or "set_reminders".

Returns:
    str: A string representing the action associated with the intent.
"""
def route_request(intent: str):
    match (intent):
        case "read_emails":
            return "Read"
        case "send_email":
            return "Send"
        case "set_reminders":
            return "Set Reminders"
