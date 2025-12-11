import os
import random
from datetime import datetime, timedelta

from services.utils import load_json, find_book_in_text


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

def reservieren(st, audio_required: bool = False):
    """
    Main Function for 'Buch reservieren' flow.
    """
    # Load Data
    books_file = os.path.join("assets", "buecher_bestand.json")
    dialogue_file = os.path.join("assets", "reservieren.json")
    
    books_data = load_json(books_file)
    dialogue_flow = load_json(dialogue_file)

    if "reservation_step" not in st.session_state or not st.session_state.messages:
        
        initial_book_context = None
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
             user_text = st.session_state.messages[-1]["content"]
             initial_book_context = find_book_in_text(user_text, books_data)
        
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
             st.session_state.messages.append({"role": "assistant", "content": msg})
             if audio_required:
                 st.session_state.audio_to_play = msg
             return

        st.session_state.reservation_step = "ask_title"
        st.session_state.reservation_book = None
        st.session_state.reservation_dates = None
        
        msg = random.choice(dialogue_flow['ask_title'])
        st.session_state.messages.append({"role": "assistant", "content": msg})
        if audio_required:
            st.session_state.audio_to_play = msg
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
                st.session_state.messages.append({"role": "assistant", "content": msg})
                if audio_required:
                    st.session_state.audio_to_play = msg
                
            else:
                # Buch nicht gefunden
                msg = random.choice(dialogue_flow['book_not_found']).format(title=user_text)
                st.session_state.messages.append({"role": "assistant", "content": msg})
                if audio_required:
                    st.session_state.audio_to_play = msg
                
        # Reservierung bestätigen
        elif st.session_state.reservation_step == "confirm_dates":
            text_lower = user_text.lower()
            if any(x in text_lower for x in ["ja", "bestätigen", "gerne", "ok", "jup"]):
                book_to_update = st.session_state.reservation_book
                new_dates = st.session_state.reservation_dates
                

                for book in books_data:
                    if book['title'] == book_to_update['title']:
                        book['available_from'] = new_dates['end'].strftime("%Y-%m-%d")
                        break
                
                save_json(books_file, books_data)
                
                msg = random.choice(dialogue_flow['success']).format(
                    title=book_to_update['title'],
                    start_date=new_dates['start'].strftime("%d.%m.%Y"),
                    end_date=new_dates['end'].strftime("%d.%m.%Y")
                )
                st.session_state.messages.append({"role": "assistant", "content": msg})
                if audio_required:
                    st.session_state.audio_to_play = msg
                
                st.session_state.reservation_step = None
                st.session_state.current_flow = None
                st.session_state.reservation_book = None
                
            elif any(x in text_lower for x in ["nein", "no", "abbruch", "nicht"]):
                msg = random.choice(dialogue_flow['cancel'])
                st.session_state.messages.append({"role": "assistant", "content": msg})
                if audio_required:
                    st.session_state.audio_to_play = msg
                
                st.session_state.reservation_step = None
                st.session_state.current_flow = None
                st.session_state.reservation_book = None
            else:
                msg = random.choice(dialogue_flow['clarify_confirmation'])
                st.session_state.messages.append({"role": "assistant", "content": msg})
                if audio_required:
                    st.session_state.audio_to_play = msg