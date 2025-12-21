import json
import os
import random
from datetime import datetime, timedelta

from services.utils import load_json, get_initial_context, send_response


def save_json(filepath, data):
    """Saves data to a JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def calculate_reservation_dates(book, duration_days=3):
    """
    Calculates start and end dates for a reservation.
    """
    today = datetime.now().date()
    available_from_str = book.get('available_from', "")
    
    if not available_from_str:
        start_date = today
    else:
        try:
            avail_date = datetime.strptime(available_from_str, "%Y-%m-%d").date()
            if avail_date <= today:
                    start_date = today
            else:
                    start_date = avail_date + timedelta(days=1)
        except ValueError:
            start_date = today
    
    end_date = start_date + timedelta(days=duration_days)
    
    return {
        "start": start_date,
        "end": end_date
    }

def process_reservation_confirmation(user_text, book_to_update, new_dates, books_data, books_file, flow_data):
    """
    Processes the user's confirmation for a reservation.
    Returns the appropriate response message.
    """
    text_lower = user_text.lower()
    
    if any(x in text_lower for x in ["ja", "bestätigen", "gerne", "ok", "jup"]):
        for book in books_data:
            if book['title'] == book_to_update['title']:
                book['available_from'] = new_dates['end'].strftime("%Y-%m-%d")
                break
        
        save_json(books_file, books_data)
        
        return random.choice(flow_data['success']).format(
            title=book_to_update['title'],
            start_date=new_dates['start'].strftime("%d.%m.%Y"),
            end_date=new_dates['end'].strftime("%d.%m.%Y")
        ), True
        
    elif any(x in text_lower for x in ["nein", "no", "abbruch", "nicht"]):
        return random.choice(flow_data['cancel']), True
        
    else:
        return random.choice(flow_data['clarify_confirmation']), False

def reservieren(st, audio_output_required: bool = False):
    """
    Main Function for 'Buch reservieren' flow.
    """
    books_file = os.path.join("assets", "buecher_bestand.json")
    dialogue_file = os.path.join("assets", "reservieren.json")
    
    books_data = load_json(books_file)
    dialogue_flow = load_json(dialogue_file)

    if "reservation_step" not in st.session_state or not st.session_state.messages:
        
        initial_book_context = get_initial_context(st, books_data)
        
        if initial_book_context:
             st.session_state.reservation_book = initial_book_context
             st.session_state.reservation_step = "confirm_dates"
             

             dates = calculate_reservation_dates(initial_book_context)
             st.session_state.reservation_dates = dates
             
             start_str = dates["start"].strftime("%d.%m.%Y")
             end_str = dates["end"].strftime("%d.%m.%Y")
             
             found_book = initial_book_context
             available_from_str = found_book.get('available_from', "")
             today = datetime.now().date()
                
             if not available_from_str or (available_from_str and dates["start"] == today):
                  msg_template = random.choice(dialogue_flow['confirm_available'])
             else:
                  msg_template = random.choice(dialogue_flow['confirm_unavailable'])
                     
             msg = msg_template.format(title=found_book['title'], start_date=start_str, end_date=end_str)
             send_response(st, msg, audio_output_required)
             return

        st.session_state.reservation_step = "ask_title"
        st.session_state.reservation_book = None
        st.session_state.reservation_dates = None
        
        msg = random.choice(dialogue_flow['ask_title'])
        send_response(st, msg, audio_output_required)
        return

    last_message = st.session_state.messages[-1]
    
    if last_message["role"] == "user":
        user_text = last_message["content"]
        
        # Schritt 1: Buch finden
        if st.session_state.reservation_step == "ask_title":
            found_book = None
            for book in books_data:
                if user_text.lower() in book['title'].lower():
                    found_book = book
                    break
            
            if found_book:
                st.session_state.reservation_book = found_book
                st.session_state.reservation_step = "confirm_dates"
     
                dates = calculate_reservation_dates(found_book)
                st.session_state.reservation_dates = dates
                
                start_str = dates["start"].strftime("%d.%m.%Y")
                end_str = dates["end"].strftime("%d.%m.%Y")
                
                available_from_str = found_book.get('available_from', "")
                today = datetime.now().date()
                
                if not available_from_str or (available_from_str and dates["start"] == today):
                     msg_template = random.choice(dialogue_flow['confirm_available'])
                else:
                     msg_template = random.choice(dialogue_flow['confirm_unavailable'])
                     
                msg = msg_template.format(title=found_book['title'], start_date=start_str, end_date=end_str)
                send_response(st, msg, audio_output_required)
                
            else:
                # Buch nicht gefunden
                msg = random.choice(dialogue_flow['book_not_found']).format(title=user_text)
                send_response(st, msg, audio_output_required)
                
        # Reservierung bestätigen
        elif st.session_state.reservation_step == "confirm_dates":
            msg, finished = process_reservation_confirmation(
                user_text, 
                st.session_state.reservation_book, 
                st.session_state.reservation_dates, 
                books_data, 
                books_file, 
                dialogue_flow
            )
            
            send_response(st, msg, audio_output_required)
            
            if finished:
                st.session_state.reservation_step = None
                st.session_state.current_flow = None
                st.session_state.reservation_book = None