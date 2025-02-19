from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def health_check():
    return {"success": True, "message": "Backend system is Active 💯..."}
