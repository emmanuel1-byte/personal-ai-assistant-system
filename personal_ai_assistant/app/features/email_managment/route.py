from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from ...helpers import validate_file, route_request
from typing import Annotated
from ...integrations import speech_to_text, get_intent
import tempfile
import os

email_management = APIRouter(prefix="/api/emails", tags=["Email-management"])


"""
Handles email-related requests by processing an uploaded audio file.

This endpoint accepts an audio file, validates its type, and processes it to
determine the user's intent. The audio file is temporarily saved, converted to
text using a speech-to-text service, and analyzed to extract the user's intent.
Based on the identified intent, an appropriate task is executed, and the
response is streamed back to the client.

Parameters:
    file (UploadFile): The audio file uploaded by the user.
    v_result (bool): The result of the file validation, injected by FastAPI's
    dependency system.

Returns:
    StreamingResponse: A streaming response containing the result of the
    requested task, with a status code of 200.
"""
@email_management.post("/")
def email(file: UploadFile, v_result: Annotated[bool, Depends(validate_file)]):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(file.file.read())
            temp_file_path = temp_file.name

            stt_response = speech_to_text(temp_file_path)
            user_intention = get_intent(stt_response)

            task_response = route_request(user_intention)
            
            return StreamingResponse(content=task_response, status_code=200)
    finally:
        os.remove(temp_file_path)
