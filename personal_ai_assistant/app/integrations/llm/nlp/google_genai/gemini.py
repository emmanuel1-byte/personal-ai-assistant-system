import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))


def get_intent(user_input):
    system_prompt = (
        "Classify the following command into one of these intents: read_emails, send_email, get_weather, set_reminder. "
        "Respond with only the intent name, nothing else."
    )
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(f"{system_prompt}\nUser command: {user_input}\nIntent:")
        return response.text.strip()
    except Exception as e:
        print(e)
