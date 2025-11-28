from services.text_2_speech import text_2_speech
import json
import os
import random

def load_json(filepath):
    """Loads a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

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
        # Book exists
        msg_template = random.choice(flow_data['book_exists'])
        msg = msg_template.format(title=found_book['title'])
        return msg
    else:
        # Book does not exist
        msg_template = random.choice(flow_data['book_not_found'])
        # Use the query as the title in the response if book not found
        msg = msg_template.format(title=title_query)
        return msg

def verfuegbarkeit_pruefen(st, used_mic: bool = False):
    """
    Main Function after intent classification for 'Verfügbarkeit prüfen'.
    Manages the flow state and user interaction.
    """
    # Load Data
    books_file = os.path.join("assets", "buecher_bestand.json")
    availability_file = os.path.join("assets", "verfuegbarkeit.json")
    
    books_data = load_json(books_file)
    availability_flow = load_json(availability_file)

    # Initialize or retrieve state for this flow
    if "availability_step" not in st.session_state or not st.session_state.messages:
        st.session_state.availability_step = "ask_title"
        # Start the conversation
        msg = random.choice(availability_flow['ask_title'])
        st.session_state.messages.append({"role": "assistant", "content": msg})
        return

    # Process user input
    last_message = st.session_state.messages[-1]
    
    if last_message["role"] == "user":
        user_text = last_message["content"]
        
        if st.session_state.availability_step == "ask_title":
            response = check_existence_logic(user_text, books_data, availability_flow)
            st.session_state.messages.append({"role": "assistant", "content": response})
            if used_mic:
                text_2_speech(response)
            
            # End flow after checking existence
            st.session_state.availability_step = None
            st.session_state.current_flow = None