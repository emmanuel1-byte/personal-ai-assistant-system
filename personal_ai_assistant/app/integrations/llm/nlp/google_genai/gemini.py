import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import re


load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def get_intent(user_input: str):
    system_prompt = (
        "Analyze the user's command carefully and determine the most appropriate intent based on its meaning. "
        "Choose from these intents: read_emails, send_email,check_schedules schedule_meeting. "
        "For example: 'Do I have any new emails?' should be classified as 'read_emails'. "
        "'Send an email to John' should be classified as 'send_email'. "
        "'Schedule a meeting for tomorrow at 10 AM' should be classified as 'schedule_meeting'. "
        "'What is my schedule like for today should be classified as 'check_schedules'. "
        "Respond strictly with only the matching intent name. If no intent clearly matches, return exactly 'None' (without quotes)."
    )
    response = model.generate_content(
        f"{system_prompt}\nUser command: {user_input}\nIntent:"
    )
    return response.text.strip()


def format_read_email_response_for_tts(gmail_response: str):
    system_prompt = (
        "You are a Gmail API formatter specialized in extracting unread email counts from Gmail API data. "
        "Your task is to analyze the provided email data and return only the count of unread emails in a natural, spoken format.\n\n"
        "### Formatting Rules:\n"
        "1. Extract only the number of unread emails.\n"
        "2. Respond in a conversational tone, e.g., 'You have 5 unread emails.'\n"
        "3. If there are no unread emails, respond with 'You have no new emails.'\n"
        "4. Do not include any additional details like sender, subject, or timestamps.\n"
        "5. Keep responses concise and clear.\n\n"
        "### Example Transformations:\n\n"
        "#### Raw Gmail API Email Data (Input)\n"
        "{\n"
        '  "messages": [\n'
        "    { 'id': '123'},\n"
        "    { 'id': '456'},\n"
        "  ]\n"
        "}\n\n"
        "#### Optimized Text-to-Speech Output (Response)\n"
        "'You have 2 unread emails.'\n\n"
        "Respond ONLY with the formatted unread email count. Do not include explanations or extra text."
    )

    response = model.generate_content(
        f"{system_prompt}\nUser command: {gmail_response}\nGmail response:"
    )
    return response.text.strip()


def generate_email_send_confirmation_message_for_tts():
    system_prompt = (
        "You are an AI communication assistant tasked with generating distinctive, contextually-appropriate email sending confirmations. "
        "Your goal is to craft memorable, concise messages that provide reassurance while maintaining a fresh and engaging tone.\n\n"
        "Key Objectives:\n"
        "1. Generate a UNIQUE confirmation message for EACH email send\n"
        "2. Vary language, structure, and emotional tone\n"
        "3. Keep responses crisp (15-25 words)\n"
        "4. Reflect the potential context of the email (professional, personal, urgent)\n\n"
        "Prohibited Patterns:\n"
        "- No verbatim repetition of previous confirmations\n"
        "- Avoid generic, bland language\n"
        "- Prevent formulaic structure across messages\n\n"
        "Examples of Diverse Confirmations:\n"
        "- 'Whoosh! Your message is soaring through cyberspace.'\n"
        "- 'Your email has landed safely in the digital mailbox.'\n"
        "- 'Message dispatched with precision. Destination: recipient's inbox.'\n\n"
        "Generate a fresh, inventive confirmation that surprises and delights."
    )

    response = model.generate_content(system_prompt)
    return response.text.strip()


def format_send_email_for_gmail(type: str, recipient: str, content: str):
    system_prompt = (
        "You are an AI assistant that generates well-structured, professional, and engaging emails. "
        "Given an email type, recipient, and content, return the response strictly in JSON format with the following: "
        "... A clear and appropriate subject line matching the email type "
        "... A polite salutation "
        "... A well-structured body "
        "... Do not include a conclusion with a name or company placeholder don't you ever do this don't ever include a place holder of any sort; never do this "
        "Ensure the tone aligns with the given email type. "
        f"Email Type: {type} "
        f"Recipient: {recipient} "
        f"Body: {content} "
        "Output format (strictly JSON, no additional text): "
        '{ "subject": "<Generated Subject>", "body": "<Generated Email Body>" }'
    )

    response = model.generate_content(system_prompt)

    try:
        email_data = json.loads(re.sub(r"^```json|```$", "", response.text).strip())
    except json.JSONDecodeError as e:
        print(f"Error: {e}")
        raise ValueError("AI response format is incorrect. Check the model's output.")
    return {
        "to": recipient,
        "subject": email_data["subject"],
        "content": email_data["body"],
    }


def format_schedule_response_for_tts(gmail_response: str):
    system_prompt = (
        "Summarize the user's email schedule from their calendar in a clear and natural way. "
        "Provide a brief but informative response suitable for a voice assistant. "
        "Use a friendly and conversational tone. If there are multiple events, list them clearly. "
        "For example, say: 'You have three meetings today. First, a project update at 10 AM, then a client call at 2 PM, and a team sync at 4 PM.' "
        "If there are no events, say: 'You have no scheduled events today.' "
        "Keep the response short, clear, and natural for text-to-speech output."
    )

    response = model.generate_content(
        f"{system_prompt}\nUser command: {gmail_response}\nGmail response:"
    )
    return response.text.strip()


def format_create_schedule_request(stt_response):
    system_prompt = (
        "Create a JSON request for the Google Calendar API based on the user's command. "
        "Extract key details such as the event title, location, description, start time, end time, time zone, "
        "recurrence pattern, attendees, and reminders. Ensure the response is structured correctly and follows "
        "Google Calendar API standards. If any required information is missing, fill in with reasonable defaults. "
        "Additionally, generate a Google Meet link dynamically for every event using a unique request ID. "
        "Use placeholders for values that need to be dynamically inserted based on user input. Format the response as JSON. "
        "Example:\n"
        "{\n"
        '  "summary": "<event_title>",\n'
        '  "location": "<event_location>",\n'
        '  "description": "<event_description>",\n'
        '  "start": {\n'
        '    "dateTime": "<start_datetime>",\n'
        '    "timeZone": "<timezone>"\n'
        "  },\n"
        '  "end": {\n'
        '    "dateTime": "<end_datetime>",\n'
        '    "timeZone": "<timezone>"\n'
        "  },\n"
        '  "recurrence": [\n'
        '    "<recurrence_rule>"\n'
        "  ],\n"
        '  "attendees": [\n'
        '    {"email": "<attendee_1>"},\n'
        '    {"email": "<attendee_2>"}\n'
        "  ],\n"
        '  "conferenceData": {\n'
        '    "createRequest": {\n'
        '      "requestId": "<random_unique_id>",\n'
        '      "conferenceSolutionKey": {\n'
        '        "type": "hangoutsMeet"\n'
        "      }\n"
        "    }\n"
        "  },\n"
        '  "reminders": {\n'
        '    "useDefault": false,\n'
        '    "overrides": [\n'
        '      {"method": "email", "minutes": <email_reminder_time>},\n'
        '      {"method": "popup", "minutes": <popup_reminder_time>}\n'
        "    ]\n"
        "  }\n"
        "}"
    )

    response = model.generate_content(
        f"{system_prompt}\nUser command: {stt_response}\nSpeech to ext response:"
    )
    try:
        event_data = json.loads(re.sub(r"^```json|```$", "", response.text).strip())
    except json.JSONDecodeError as e:
        print(f"Error: {e}")
        raise ValueError("AI response format is incorrect. Check the model's output.")

    return event_data
