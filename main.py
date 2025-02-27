from fastapi import FastAPI
from personal_ai_assistant.app.features import email_management

app = FastAPI()

app.include_router(email_management)


@app.get("/")
def health_check():
    return {"success": True, "message": "Backend system is Active 💯..."}
