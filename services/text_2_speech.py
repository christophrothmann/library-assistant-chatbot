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


def text_2_speech(text: str) -> None:
    elevenlabs = init_elevenlabs()

    audio = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id="v3V1d2rk6528UrLKRuy8",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    play(audio)
