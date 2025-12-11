import os
import random

from services.text_2_speech import text_2_speech
from services.utils import load_json, find_book_in_text


def regalsuche(st, audio_required: bool = False):
    """
    Main Function for 'Buch lokalisieren' flow.
    """
    # Load Data
    books_file = os.path.join("assets", "buecher_bestand.json")
    dialogue_file = os.path.join("assets", "regalsuche.json")
    
    books_data = load_json(books_file)
    dialogue_flow = load_json(dialogue_file)

    if "regalsuche_step" not in st.session_state or not st.session_state.messages:
        
        initial_book_context = None
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
             user_text = st.session_state.messages[-1]["content"]
             initial_book_context = find_book_in_text(user_text, books_data)
        
        if initial_book_context:
            found_book = initial_book_context
            msg = random.choice(dialogue_flow['found_location']).format(
                title=found_book['title'],
                floor=found_book['floor'],
                shelf_name=found_book['shelf_name'],
                shelf_height=found_book['shelf_height']
            )
            st.session_state.messages.append({"role": "assistant", "content": msg})
            if audio_required:
                st.session_state.audio_to_play = msg

            st.session_state.regalsuche_step = None
            st.session_state.current_flow = None
            return
        st.session_state.regalsuche_step = "ask_title"
        
        msg = random.choice(dialogue_flow['ask_title'])
        st.session_state.messages.append({"role": "assistant", "content": msg})
        if audio_required:
            st.session_state.audio_to_play = msg
        return

    last_message = st.session_state.messages[-1]
    
    if last_message["role"] == "user":
        user_text = last_message["content"]
        
        if st.session_state.regalsuche_step == "ask_title":
            found_book = None
            for book in books_data:
                if user_text.lower() in book['title'].lower():
                    found_book = book
                    break
            
            if found_book:
                msg = random.choice(dialogue_flow['found_location']).format(
                    title=found_book['title'],
                    floor=found_book['floor'],
                    shelf_name=found_book['shelf_name'],
                    shelf_height=found_book['shelf_height']
                )
                st.session_state.messages.append({"role": "assistant", "content": msg})
                if audio_required:
                    text_2_speech(msg)
            else:
                msg = random.choice(dialogue_flow['book_not_found']).format(title=user_text)
                st.session_state.messages.append({"role": "assistant", "content": msg})
                if audio_required:
                    text_2_speech(msg)
            
            st.session_state.regalsuche_step = None
            st.session_state.current_flow = None