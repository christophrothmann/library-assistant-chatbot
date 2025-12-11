import os
import random

from services.utils import load_json, get_initial_context, send_response


def format_shelf_location_msg(book, flow_data):
    """Formats the shelf location message using the book data."""
    return random.choice(flow_data['found_location']).format(
        title=book['title'],
        floor=book['floor'],
        shelf_name=book['shelf_name'],
        shelf_height=book['shelf_height']
    )

def regalsuche(st, audio_required: bool = False):
    """
    Main Function for 'Buch lokalisieren' flow.
    """
    
    
    books_file = os.path.join("assets", "buecher_bestand.json")
    dialogue_file = os.path.join("assets", "regalsuche.json")
    
    books_data = load_json(books_file)
    dialogue_flow = load_json(dialogue_file)

    if "regalsuche_step" not in st.session_state or not st.session_state.messages:
        
        initial_book_context = get_initial_context(st, books_data)
        
        if initial_book_context:
            found_book = initial_book_context
            msg = format_shelf_location_msg(found_book, dialogue_flow)
            send_response(st, msg, audio_required)

            st.session_state.regalsuche_step = None
            st.session_state.current_flow = None
            return
        st.session_state.regalsuche_step = "ask_title"
        
        msg = random.choice(dialogue_flow['ask_title'])
        send_response(st, msg, audio_required)
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
                msg = format_shelf_location_msg(found_book, dialogue_flow)
                send_response(st, msg, audio_required)
            else:
                msg = random.choice(dialogue_flow['book_not_found']).format(title=user_text)
                send_response(st, msg, audio_required)
            
            st.session_state.regalsuche_step = None
            st.session_state.current_flow = None