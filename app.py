import streamlit as st
import json
import os
import datetime
from datetime import timedelta
import speech_recognition as sr

st.set_page_config(page_title="Goleo - Bibliotheksassistent", page_icon="📚")


# --- Main App ---
def main():
    st.title("Goleo - Dein Bibliotheksassistent")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    with st.sidebar:
        st.header("Schnellaktionen")
        
        def reset_chat():
            st.session_state.messages = []

        if st.button("Verfügbarkeitsstatus prüfen", use_container_width=True):
            reset_chat()
            st.rerun()
            
        if st.button("Buch reservieren", use_container_width=True):
            reset_chat()
            st.rerun()
            
        if st.button("Buch lokalisieren", use_container_width=True):
            reset_chat()
            st.rerun()
            
        if st.button("Texttreffer in Büchern", use_container_width=True):
            reset_chat()
            st.rerun()

    # Helper to process user input
    def process_input(user_text):
        if not user_text:
            return
        
        st.session_state.messages.append({"role": "user", "content": user_text})
        
    
    if not st.session_state.messages:
        st.markdown("""
        Hallo! Ich bin **Goleo**, dein Assistent für die Bibliothek.
        Wähle eine Aktion aus der Sidebar, um zu starten.
        """)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    st.divider()
    input_col, mic_col = st.columns([8, 1])
    
    with input_col:
        # Callback to handle "Enter" key
        def on_text_submit():
            txt = st.session_state.user_input_widget
            if txt:
                process_input(txt)
                st.session_state.user_input_widget = "" # Clear input

        st.text_input(
            "Nachricht", 
            key="user_input_widget", 
            label_visibility="collapsed", 
            placeholder="Schreibe eine Nachricht...",
            on_change=on_text_submit
        )

    with mic_col:
        # Use Material Icon
        if st.button("", icon=":material/mic:"):
            transcribed_text = listen_and_transcribe()
            if transcribed_text:
                process_input(transcribed_text)
                st.rerun()

if __name__ == "__main__":
    main()
