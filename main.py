from fastapi import FastAPI
from personal_ai_assistant.app.features import email_management
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(email_management)


@app.get("/")
def health_check():
    return {"success": True, "message": "Backend system is Active 💯..."}
