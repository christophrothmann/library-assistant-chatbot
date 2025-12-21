from functools import lru_cache
import json


@lru_cache(maxsize=2)
def load_json(filepath):
    """Loads a JSON file. Returns an empty dict or list depending on file content if error."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def find_book_in_text(text, books_data):
    """
    Checks if any book title from books_data is present in the text.
    Returns the book object if found, else None.
    """
    if not text:
        return None
    
    text_lower = text.lower()
    found_book = None
    best_match_len = 0

    for book in books_data:
        current_match_len = 0
        match_found = False
        
        if book['title'].lower() in text_lower:
            current_match_len = len(book['title'])
            match_found = True
            
        authors = book['author'].replace(';', ',').split(',')
        for auth_part in authors:
            auth_cl = auth_part.strip().lower()
            if len(auth_cl) > 3 and auth_cl in text_lower:
                if len(auth_cl) > current_match_len:
                    current_match_len = len(auth_cl)
                    match_found = True

        if text_lower in book['title'].lower() and len(text_lower) > 4:
             if len(text_lower) > current_match_len:
                current_match_len = len(text_lower)
                match_found = True

        if match_found:
            if current_match_len > best_match_len:
                best_match_len = current_match_len
                found_book = book
            
    return found_book

def get_initial_context(st, books_data):
    """
    Checks the last user message for a book title using find_book_in_text.
    Returns the book object or None.
    """
    initial_book_context = None
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
         user_text = st.session_state.messages[-1]["content"]
         initial_book_context = find_book_in_text(user_text, books_data)
    return initial_book_context

def send_response(st, message, audio_output_required=False):
    """
    Appends the message to session state and sets audio to play if required.
    """
    st.session_state.messages.append({"role": "assistant", "content": message})
    if audio_output_required:
        st.session_state.audio_to_play = message

