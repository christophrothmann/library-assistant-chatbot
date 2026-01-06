import streamlit as st

from services.buchsuche import buchsuche
from services.intent_classifier import classify_intent
from services.regalsuche import regalsuche
from services.reservieren import reservieren
from services.speech_2_text import listen_and_transcribe
from services.text_2_speech import generate_audio, play_audio
from services.verfuegbarkeit import verfuegbarkeit_pruefen

st.set_page_config(page_title="Goleo - Dein Bibliotheksassistent", page_icon="./assets/goleo.png")

def main():
    st.title("Goleo - Dein Bibliotheksassistent")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "current_flow" not in st.session_state:
        st.session_state.current_flow = None
    
    if "step" not in st.session_state:
        st.session_state.step = None
        
    if "context_book" not in st.session_state:
        st.session_state.context_book = None
        
    if "audio_to_play" not in st.session_state:
        st.session_state.audio_to_play = None

    with st.sidebar:
        st.header("Schnellaktionen")
        
        def reset_chat():
            st.session_state.messages = []
            st.session_state.current_flow = None
            st.session_state.step = None
            st.session_state.context_book = None

        if st.button(label="Neuen Chat beginnen", use_container_width=True):
            reset_chat()
            st.rerun()    

        if st.button("Verfügbarkeitsstatus prüfen", use_container_width=True):
            reset_chat()
            st.session_state.current_flow = "verfuegbarkeit_pruefen"
            verfuegbarkeit_pruefen(st)
            st.rerun()
            
        if st.button("Buch reservieren", use_container_width=True):
            reset_chat()
            st.session_state.current_flow = "reservieren"
            reservieren(st)
            st.rerun()
            
        if st.button("Buch lokalisieren", use_container_width=True):
            reset_chat()
            st.session_state.current_flow = "regalsuche"
            regalsuche(st)
            st.rerun()
            
        if st.button("Texttreffer in Büchern", use_container_width=True):
            reset_chat()
            st.session_state.current_flow = "buchsuche"
            buchsuche(st)
            st.rerun()
        st.divider()
        st.checkbox("Audioausgabe aktivieren", key="audio_enabled")

    def process_input(user_text, used_mic: bool = False):
        if not user_text:
            return
        
        st.session_state.messages.append({"role": "user", "content": user_text})

        if not st.session_state.get("current_flow"):
            classified_intent = classify_intent(user_text)
            print(f"Klassifizierte Absicht: {classified_intent}")
            if classified_intent == "capabilities":
                response = "Ich kann so einiges. Ich kann die Verfügbarkeit von Büchern prüfen, Bücher reservieren, Bücher lokalisieren und nach Text in Büchern suchen. Sag mir einfach, was du tun möchtest!"
                st.session_state.messages.append({"role": "assistant", "content": response})
                if st.session_state.get("audio_enabled", False):
                     st.session_state.audio_to_play = response
            elif classified_intent == "greeting":
                response = "Hallo! Ich bin Goleo. Wie kann ich dir behilflich sein?"
                st.session_state.messages.append({"role": "assistant", "content": response})
                if st.session_state.get("audio_enabled", False):
                     st.session_state.audio_to_play = response
            elif classified_intent:
                st.session_state.current_flow = classified_intent

        should_speak = st.session_state.get("audio_enabled", False)
        
        if st.session_state.get("current_flow") == "verfuegbarkeit_pruefen":
             verfuegbarkeit_pruefen(st, should_speak)
        elif st.session_state.get("current_flow") == "reservieren":
             reservieren(st, should_speak)
        elif st.session_state.get("current_flow") == "regalsuche":
             regalsuche(st, should_speak)
        elif st.session_state.get("current_flow") == "buchsuche":
             buchsuche(st, should_speak)
        
        
    if not st.session_state.messages:
        st.markdown("""
        Hallo! Ich bin **Goleo**, dein Assistent für die Bibliothek.
        Wähle eine Aktion aus der Sidebar, um zu starten oder verwende die Text- /Spracheingabe.
        """)

    audio_path_to_play = None
    if st.session_state.get("audio_to_play"):
        with st.spinner("Generiere Antwort..."):
            audio_path_to_play = generate_audio(st.session_state.audio_to_play)
        st.session_state.audio_to_play = None

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    st.divider()
    input_col, mic_col = st.columns([8, 1])
    
    with input_col:
        def on_text_submit():
            txt = st.session_state.user_input_widget
            if txt:
                process_input(txt, used_mic=False)
                st.session_state.user_input_widget = ""

        st.text_input(
            "Nachricht", 
            key="user_input_widget", 
            label_visibility="collapsed", 
            placeholder="Schreibe eine Nachricht...",
            on_change=on_text_submit,
        )

    with mic_col:
        if st.button("", icon=":material/mic:"):
            transcribed_text = listen_and_transcribe(st)
            if transcribed_text:
                process_input(transcribed_text, used_mic=True)
                st.rerun()

    if audio_path_to_play:
        play_audio(audio_path_to_play)

if __name__ == "__main__":
    main()
