from functools import lru_cache
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os


@lru_cache(maxsize=1)
def init_elevenlabs():
    load_dotenv()
    return ElevenLabs(
        api_key=os.getenv("ELEVENLABS_API_KEY"),
    )


def generate_audio(text: str) -> bytes:
    elevenlabs = init_elevenlabs()
    audio = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id="v3V1d2rk6528UrLKRuy8",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    return b"".join(audio)

def play_audio(audio_bytes: bytes) -> None:
    play(audio_bytes)

def text_2_speech(text: str) -> None:
    audio_bytes = generate_audio(text)
    play_audio(audio_bytes)
