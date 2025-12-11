import os
import random

from services.utils import load_json


def search_books(keyword, books_data):
    """
    Searches for books containing the keyword in title, author, or summary.
    Returns a list of matching book objects.
    """
    matches = []
    keyword_lower = keyword.lower()
    
    for book in books_data:
        if (keyword_lower in book['title'].lower() or 
            keyword_lower in book['author'].lower() or 
            keyword_lower in book['summary'].lower()):
            matches.append(book)
    return matches

def format_results(matches):
    """
    Formats a list of book objects into a string.
    """
    if not matches:
        return ""
    
    result_str = ""
    for i, book in enumerate(matches, 1):
        result_str += f"{i}. **{book['title']}** von {book['author']}\n   _{book['summary']}_\n\n"
    return result_str

def buchsuche(st, audio_required: bool = False):
    """
    Main Function after intent classification for 'Buchsuche'.
    Manages the flow state and user interaction.
    """
    # Die "buecher_bestand.json" Datei wurde von KI generiert
    books_file = os.path.join("assets", "buecher_bestand.json")
    search_file = os.path.join("assets", "buchsuche.json")
    
    books_data = load_json(books_file)
    search_flow = load_json(search_file)

    if "buchsuche_step" not in st.session_state or not st.session_state.messages:
        
        # Context Check
        # If we came from intent classifier with input, use that as query.
        initial_query = None
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
             initial_query = st.session_state.messages[-1]["content"]
        
        if initial_query:
            matches = search_books(initial_query, books_data)
            
            if matches:
                result_list = format_results(matches)
                msg_template = random.choice(search_flow['results_found'])
                response = msg_template.format(results=result_list)
            else:
                msg_template = random.choice(search_flow['no_results'])
                response = msg_template.format(keyword=initial_query)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            if audio_required:
                st.session_state.audio_to_play = response
            
       
            st.session_state.buchsuche_step = None
            st.session_state.current_flow = None
            return

        st.session_state.buchsuche_step = "ask_keyword"
        
        msg = random.choice(search_flow['ask_keyword'])
        st.session_state.messages.append({"role": "assistant", "content": msg})
        if audio_required:
             st.session_state.audio_to_play = msg
        return

    last_message = st.session_state.messages[-1]
    
    if last_message["role"] == "user":
        user_text = last_message["content"]
        
        if st.session_state.buchsuche_step == "ask_keyword":
            matches = search_books(user_text, books_data)
            
            if matches:
                result_list = format_results(matches)
                msg_template = random.choice(search_flow['results_found'])
                response = msg_template.format(results=result_list)
            else:
                msg_template = random.choice(search_flow['no_results'])
                response = msg_template.format(keyword=user_text)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            if audio_required:
                st.session_state.audio_to_play = response
            
            # End flow after showing results
            st.session_state.buchsuche_step = None
            st.session_state.current_flow = None