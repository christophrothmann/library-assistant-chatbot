import json


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
    Prioritizes longer titles to avoid partial matches (logic to be improved if needed).
    """
    if not text:
        return None
    
    text_lower = text.lower()
    found_book = None
    

    sorted_books = sorted(books_data, key=lambda x: len(x['title']), reverse=True)
    
    for book in sorted_books:
        if book['title'].lower() in text_lower:
            found_book = book
            break
            
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

def send_response(st, message, audio_required=False):
    """
    Appends the message to session state and sets audio to play if required.
    """
    st.session_state.messages.append({"role": "assistant", "content": message})
    if audio_required:
        st.session_state.audio_to_play = message

