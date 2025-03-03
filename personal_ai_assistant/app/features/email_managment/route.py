from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from ...helpers import validate_file, route_request
from typing import Annotated
from ...integrations import (
    speech_to_text,
    get_intent,
    text_to_speech,
)
import tempfile
import os

email_management = APIRouter(prefix="/api/emails", tags=["Email-management"])



"""
Handles the POST request to process an uploaded audio file.

This endpoint accepts an audio file, validates its type, and processes it
to determine the user's intent. The audio is converted to text, classified
into an intent, and routed to the appropriate handler. The response is then
converted to speech and streamed back to the client.

Args:
    file (UploadFile): The audio file uploaded by the user.
    v_result (bool): Validation result of the uploaded file type.

Returns:
    StreamingResponse: The audio response generated from the processed intent.
"""
@email_management.post("/")
def email(file: UploadFile, v_result: Annotated[bool, Depends(validate_file)]):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(file.file.read())
            temp_file_path = temp_file.name

            text_response = speech_to_text(temp_file_path)
            user_intention = get_intent(text_response)

            router_response = route_request(user_intention)
            print(router_response, "Router Response....")
            tts_response = text_to_speech(router_response)

            return StreamingResponse(content=tts_response, media_type="audio/wav", status_code=200)
    finally:
        os.remove(temp_file_path)
