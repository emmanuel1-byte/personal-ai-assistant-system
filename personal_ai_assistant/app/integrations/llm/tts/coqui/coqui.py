import torch
from TTS.api import TTS
from io import BytesIO
import soundfile as sf


"""
Convert input text to speech and return the audio as a WAV file in a buffer.

This function utilizes a TTS model to synthesize speech from the provided text.
The audio is processed on a CUDA-enabled GPU if available, otherwise on the CPU.
The resulting audio is stored in a BytesIO buffer in WAV format.

Args:
    text (str): The input text to be converted to speech.

Returns:
    BytesIO: A buffer containing the synthesized speech in WAV format.
"""
def text_to_speech(text):
    print(text, "Text................")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS(model_name="tts_models/en/ljspeech/vits", progress_bar=False).to(device)

    wav = tts.tts(text)

    buffer = BytesIO()
    sf.write(buffer, wav, samplerate=22050, format="WAV")
    buffer.seek(0)

    return buffer
