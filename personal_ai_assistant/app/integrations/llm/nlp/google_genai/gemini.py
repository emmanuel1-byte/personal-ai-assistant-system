import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def get_intent(user_input):
    system_prompt = (
        "Classify the following command into one of these intents: read_emails, send_email, set_reminder. "
        "Respond with only the intent name, nothing else."
    )
    try:
        response = model.generate_content(
            f"{system_prompt}\nUser command: {user_input}\nIntent:"
        )
        return response.text.strip()
    except Exception as e:
        print(e)


def format_read_email_response_for_tts(gmail_response):
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

    try:
        response = model.generate_content(
            f"{system_prompt}\nUser command: {gmail_response}\nGmail response:"
        )
        return response.text.strip()
    except Exception as e:
        print(e)
