from fastapi import UploadFile, HTTPException


"""
Validates the MIME type of an uploaded file.

Parameters:
    file (UploadFile): The file to be validated.

Raises:
    HTTPException: If the file's MIME type is not one of the allowed types.

Returns:
    bool: True if the file's MIME type is valid.
"""
def validate_file(file: UploadFile):
    allowed_mime_types = ["audio/wav", "audio/ogg", "audio/mp3"]
    if file.content_type not in allowed_mime_types:
        raise HTTPException(status_code=400, detail="Invalid file type")
    return True
