import asyncio
import edge_tts
import pygame
import os

# Voice Configuration
VOICE = "de-DE-AmalaNeural"
RATE = "+15%"
PITCH = "-2Hz" # Adjusted slightly from snippet for better neutrality, or keep user's preferences? User had +15%, -5Hz. I'll stick close to user's snippet but maybe slightly clearer. Let's use user's: +15%, -5Hz.

async def _generate_audio_async(text: str, output_file: str) -> None:
    communicate = edge_tts.Communicate(text, voice=VOICE, rate="+15%", pitch="-5Hz")
    await communicate.save(output_file)

def generate_audio(text: str) -> str:
    """
    Generates audio from text using Edge TTS and saves it to a temporary file.
    Returns the path to the saved file.
    """
    # Ensure assets directory exists
    os.makedirs("assets", exist_ok=True)
    filename = "./assets/temp_audio.mp3"
    
    # Remove existing file if it exists
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except OSError:
            pass # File might be in use, ignore for now
        
    try:
        asyncio.run(_generate_audio_async(text, filename))
    except Exception as e:
        print(f"Error generating audio: {e}")
        return ""
        
    return filename

def play_audio(file_path: str) -> None:
    """
    Plays the audio file at the given path using pygame.
    """
    if not os.path.exists(file_path):
        return

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        # cleanup
        pygame.mixer.quit()
    except Exception as e:
        print(f"Error playing audio: {e}")

def text_2_speech(text: str) -> None:
    """
    Legacy wrapper.
    """
    file_path = generate_audio(text)
    play_audio(file_path)



