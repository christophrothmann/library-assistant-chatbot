from services.intent_classifier import classify_intent
from services.buchsuche import buchsuche
from services.regalsuche import regalsuche
from services.reservieren import reservieren
from services.verfuegbarkeit import verfuegbarkeit_pruefen
from services.speech_2_text import listen_and_transcribe
import streamlit as st
import json
import os
import datetime
from datetime import timedelta


# --- Configuration & Setup ---
st.set_page_config(page_title="Goleo - Bibliotheksassistent", page_icon="📚")

# --- Main App ---
def main():
    st.title("Goleo - Dein Bibliotheksassistent")

    # Initialize Session State
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "current_flow" not in st.session_state:
        st.session_state.current_flow = None # None, 'availability', etc.
    
    if "step" not in st.session_state:
        st.session_state.step = None
        
    if "context_book" not in st.session_state:
        st.session_state.context_book = None

    with st.sidebar:
        st.header("Schnellaktionen")
        
        def reset_chat():
            st.session_state.messages = []
            st.session_state.current_flow = None
            st.session_state.step = None
            st.session_state.context_book = None

        if st.button(label="Neuer Chat beginnen", use_container_width=True):
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

    # Helper to process user input
    def process_input(user_text, used_mic: bool = False):
        if not user_text:
            return
        
        st.session_state.messages.append({"role": "user", "content": user_text})

        # If no flow is active, try to classify intent
        if not st.session_state.get("current_flow"):
            classified_intent = classify_intent(user_text)
            # Only switch if a valid intent is found (assuming classifier always returns something, 
            # but we might want to handle 'None' if we had a fallback, 
            # currently it forces one of the known intents)
            if classified_intent:
                st.session_state.current_flow = classified_intent

        # Dispatch to the active flow
        if st.session_state.get("current_flow") == "verfuegbarkeit_pruefen":
             verfuegbarkeit_pruefen(st, used_mic)
        elif st.session_state.get("current_flow") == "reservieren":
             reservieren(st, used_mic)
        elif st.session_state.get("current_flow") == "regalsuche":
             regalsuche(st, used_mic)
        elif st.session_state.get("current_flow") == "buchsuche":
             buchsuche(st, used_mic)
        
        
    # --- Welcome Screen ---
    if not st.session_state.messages:
        st.markdown("""
        Hallo! Ich bin **Goleo**, dein Assistent für die Bibliothek.
        Wähle eine Aktion aus der Sidebar, um zu starten oder verwende die Text- /Spracheingabe.
        """)

    # --- Chat History Display ---
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- Input Area ---
    # Layout: [Text Input] [Mic Button]
    st.divider()
    input_col, mic_col = st.columns([8, 1])
    
    with input_col:
        # Callback to handle "Enter" key
        def on_text_submit():
            txt = st.session_state.user_input_widget
            if txt:
                process_input(txt, used_mic=False)
                st.session_state.user_input_widget = "" # Clear input

        st.text_input(
            "Nachricht", 
            key="user_input_widget", 
            label_visibility="collapsed", 
            placeholder="Schreibe eine Nachricht...",
            on_change=on_text_submit,
        )

    with mic_col:
        # Use Material Icon
        if st.button("", icon=":material/mic:"):
            transcribed_text = listen_and_transcribe(st)
            if transcribed_text:
                process_input(transcribed_text, used_mic=True)
                st.rerun()

if __name__ == "__main__":
    main()
