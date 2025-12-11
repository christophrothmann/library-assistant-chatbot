import os
import random

from services.utils import load_json, get_initial_context, send_response


def check_existence_logic(title_query, books_data, flow_data):
    """
    Checks if a book exists in the inventory and returns a random response message.
    """
    found_book = None
    for book in books_data:
        if title_query.lower() in book['title'].lower():
            found_book = book
            break
    
    if found_book:
        msg_template = random.choice(flow_data['book_exists'])
        msg = msg_template.format(title=found_book['title'])
        return msg
    else:
        msg_template = random.choice(flow_data['book_not_found'])
        msg = msg_template.format(title=title_query)
        return msg

def verfuegbarkeit_pruefen(st, audio_required: bool = False):
    """
    Main Function after intent classification for 'Verfügbarkeit prüfen'.
    Manages the flow state and user interaction.
    """

    books_file = os.path.join("assets", "buecher_bestand.json")
    availability_file = os.path.join("assets", "verfuegbarkeit.json")
    
    books_data = load_json(books_file)
    availability_flow = load_json(availability_file)

    if "availability_step" not in st.session_state or not st.session_state.messages:
        initial_book_context = get_initial_context(st, books_data)
        
        if initial_book_context:
            st.session_state.availability_step = "check_existence"
            response = check_existence_logic(initial_book_context['title'], books_data, availability_flow)
            send_response(st, response, audio_required)
            
            st.session_state.availability_step = None
            st.session_state.current_flow = None
            return
        else:
            st.session_state.availability_step = "ask_title"
            msg = random.choice(availability_flow['ask_title'])
            send_response(st, msg, audio_required)
            return

    last_message = st.session_state.messages[-1]
    
    if last_message["role"] == "user":
        user_text = last_message["content"]
        
        if st.session_state.availability_step == "ask_title":
            response = check_existence_logic(user_text, books_data, availability_flow)
            send_response(st, response, audio_required)
            
            st.session_state.availability_step = None
            st.session_state.current_flow = None