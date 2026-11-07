import os
import tempfile
from dotenv import load_dotenv
from gnani.stt import GnaniSTTClient
from gnani.tts import GnaniTTSClient, AudioConfig

load_dotenv()

def _api_key():
    key = os.getenv("GNANI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("GNANI_API_KEY is missing. Add it to your .env file.")
    return key

def get_api_status():
    if os.getenv("GNANI_API_KEY", "").strip():
        return True, "API key found."
    return False, "Add GNANI_API_KEY=your_key to .env and restart Streamlit."

def transcribe_audio(audio_bytes: bytes, language_code: str):
    """Send recorded audio to Gnani Prisma and return transcript."""
    if not audio_bytes:
        raise ValueError("No audio was recorded.")
    client = GnaniSTTClient(api_key=_api_key())
    suffix = ".wav"
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            temp.write(audio_bytes)
            temp_path = temp.name
        result = client.transcribe(temp_path, language_code=language_code)
        transcript = result.get("transcript", "").strip()
        if not transcript:
            raise RuntimeError(f"Prisma returned no transcript. Response: {result}")
        return transcript, result.get("detected_language_code", language_code)
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

def synthesize_speech(text: str, language_code: str) -> bytes:
    """Generate speech with Gnani Timbre v2.5."""
    if not text.strip():
        raise ValueError("Text is empty.")
    client = GnaniTTSClient(api_key=_api_key())

    # Change these in .env if your account exposes different voice names.
    voice_map = {
        "te-IN": os.getenv("GNANI_TTS_VOICE_TE", "Kaveri"),
        "hi-IN": os.getenv("GNANI_TTS_VOICE_HI", "Nalini"),
        "en-IN": os.getenv("GNANI_TTS_VOICE_EN", "Kaveri"),
        "ta-IN": os.getenv("GNANI_TTS_VOICE_TA", "Kaveri"),
    }
    voice = voice_map.get(language_code, "Kaveri")
    audio = client.synthesize(
        text[:3000],
        voice=voice,
        model="timbre-v2.5",
        language=language_code,
        speed=1.0,
        audio_config=AudioConfig(
            sample_rate=48000,
            container="wav",
            encoding="linear_pcm"
        )
    )
    return audio
