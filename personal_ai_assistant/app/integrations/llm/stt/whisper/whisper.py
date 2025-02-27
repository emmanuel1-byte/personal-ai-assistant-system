import whisper

"""
Transcribes speech from an audio file to text using the Whisper model.

Args:
    audio_file (str): The path to the audio file to be transcribed.

Returns:
    str: The transcribed text from the audio file.
"""
def speech_to_text(audio_file):
    model = whisper.load_model("tiny.en")
    response = model.transcribe(audio_file)
    return response["text"]
