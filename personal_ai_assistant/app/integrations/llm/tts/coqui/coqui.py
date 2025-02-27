import torch
from TTS.api import TTS


"""
Converts the given text to speech and saves it to a file.

This function utilizes a TTS model to generate speech from the input text.
It selects the appropriate device (CUDA or CPU) for processing based on
availability. The function lists available TTS models and uses a specific
German TTS model for conversion.

Args:
    text (str): The text to be converted to speech.

Returns:
    str: The file path where the generated speech is saved.
"""
def text_to_speech(text):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC", progress_bar=False).to(
        device
    )
    return tts.tts_to_file(text)
