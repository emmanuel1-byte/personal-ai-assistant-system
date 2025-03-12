from fastapi import APIRouter, UploadFile, Depends, Form
from fastapi.responses import JSONResponse, StreamingResponse
from ...helpers import validate_file, route_request, valid_url
from typing import Annotated
from ...integrations import (
    speech_to_text,
    get_intent,
    text_to_speech,
)
import re
import tempfile
import os
from typing import Optional, Annotated
from .enum import Email_Provider, Email_Type

email_management = APIRouter(prefix="/api/tasks", tags=["Task-management"])


"""
Handles the POST request to process an email-related audio file.

This endpoint accepts an audio file, validates it, and processes it to determine
the user's intent. It supports optional form data for specifying the email type,
provider, and recipient. The audio file is converted to text, the intent is
determined, and an appropriate action is taken based on the intent. The response
is returned as an audio stream.

Parameters:
    file (UploadFile): The audio file to be processed.
    v_result (bool): Validation result of the uploaded file.
    email_type (Optional[Email_Type]): The type of email, if specified.
    email_provider (Optional[Email_Provider]): The email provider, if specified.
    email_recipeint (Optional[str]): The email recipient, if specified.

Returns:
    StreamingResponse: An audio response indicating the result of the processed
    request.
"""


@email_management.post("/")
def email(
    file: UploadFile,
    v_result: Annotated[bool, Depends(validate_file)],
    email_type: Annotated[Optional[Email_Type], Form()] = None,
    email_provider: Annotated[Optional[Email_Provider], Form()] = None,
    email_recipeint: Annotated[Optional[str], Form()] = None,
):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(file.file.read())
            temp_file_path = temp_file.name

            text_response = speech_to_text(temp_file_path)
            user_intention = get_intent(text_response)
            
            print(user_intention, "..............")

            if user_intention == "None":
                tts_response = text_to_speech(
                    "I'm not sure what you mean. Please try again with a clear request."
                )
            else:
                router_response = route_request(
                    user_intention,
                    {
                        "type": email_type.value if email_type else email_type,
                        "email": email_recipeint,
                        "provider": (
                            email_provider.value if email_provider else email_provider
                        ),
                        "content": text_response,
                    },
                )

                if valid_url(router_response):
                    return JSONResponse(content=router_response, status_code=200)
                else:
                    tts_response = text_to_speech(router_response)
                    return StreamingResponse(
                        content=tts_response, media_type="audio/wav", status_code=200
                    )
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        os.remove(temp_file_path)
