import speech_recognition as sr

def listen_and_transcribe(st):
    """
    Listens to the microphone and transcribes speech to text using SpeechRecognition.
    Returns the recognized text or None if failed.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.toast("Ich höre zu... Sprich jetzt!", icon="🎤")
        try:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            st.toast("Verarbeite...", icon="🔄")
            text = r.recognize_google(audio, language="de-DE")
            return text
        except sr.WaitTimeoutError:
            st.toast("Keine Spracheingabe erkannt.", icon=" ")
            return None
        except sr.UnknownValueError:
            st.toast("Ich konnte das leider nicht verstehen.", icon=" ")
            return None
        except sr.RequestError as e:
            st.toast(f"Fehler: {e}", icon=" ")
            return None
        except Exception as e:
            st.toast(f"Fehler: {e}", icon=" ")
            return None
