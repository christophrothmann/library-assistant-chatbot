import json
import os
import random
from datetime import datetime, timedelta

def load_json(filepath):
    """Loads a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_json(filepath, data):
    """Saves data to a JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def reservieren(st, used_mic: bool = False):
    """
    Main Function for 'Buch reservieren' flow.
    """
    # Load Data
    books_file = os.path.join("assets", "buecher_bestand.json")
    dialogue_file = os.path.join("assets", "reservieren.json")
    
    books_data = load_json(books_file)
    dialogue_flow = load_json(dialogue_file)

    # Initialize state
    if "reservation_step" not in st.session_state or not st.session_state.messages:
        st.session_state.reservation_step = "ask_title"
        st.session_state.reservation_book = None
        st.session_state.reservation_dates = None
        
        msg = random.choice(dialogue_flow['ask_title'])
        st.session_state.messages.append({"role": "assistant", "content": msg})
        if used_mic:
            text_2_speech(msg)
        return

    # Process user input
    last_message = st.session_state.messages[-1]
    
    if last_message["role"] == "user":
        user_text = last_message["content"]
        
        # Step 1: Find Book
        if st.session_state.reservation_step == "ask_title":
            found_book = None
            for book in books_data:
                if user_text.lower() in book['title'].lower():
                    found_book = book
                    break
            
            if found_book:
                st.session_state.reservation_book = found_book
                st.session_state.reservation_step = "confirm_dates"
                
                # Calculate Dates
                today = datetime.now().date()
                available_from_str = found_book.get('available_from', "")
                
                if not available_from_str:
                    # Available now
                    start_date = today
                else:
                    # Currently borrowed
                    try:
                        avail_date = datetime.strptime(available_from_str, "%Y-%m-%d").date()
                        if avail_date <= today:
                             start_date = today
                        else:
                             start_date = avail_date + timedelta(days=1)
                    except ValueError:
                        start_date = today # Fallback
                
                end_date = start_date + timedelta(days=3)
                
                # Store dates for confirmation
                st.session_state.reservation_dates = {
                    "start": start_date,
                    "end": end_date
                }
                
                # Format dates for display
                start_str = start_date.strftime("%d.%m.%Y")
                end_str = end_date.strftime("%d.%m.%Y")
                
                if not available_from_str or (available_from_str and start_date == today):
                     msg_template = random.choice(dialogue_flow['confirm_available'])
                else:
                     msg_template = random.choice(dialogue_flow['confirm_unavailable'])
                     
                msg = msg_template.format(title=found_book['title'], start_date=start_str, end_date=end_str)
                st.session_state.messages.append({"role": "assistant", "content": msg})
                if used_mic:
                    st.session_state.audio_to_play = msg
                
            else:
                # Book not found
                msg = random.choice(dialogue_flow['book_not_found']).format(title=user_text)
                st.session_state.messages.append({"role": "assistant", "content": msg})
                if used_mic:
                    st.session_state.audio_to_play = msg
                # Reset or ask again? Let's stay in ask_title or exit. 
                # For simplicity, let's reset flow or just ask again. 
                # The user might want to try another title.
                # Let's keep state as ask_title but maybe user wants to exit.
                # For now, just wait for next input which will be treated as title.
                
        # Step 2: Confirm Reservation
        elif st.session_state.reservation_step == "confirm_dates":
            # Simple Yes/No detection
            text_lower = user_text.lower()
            if any(x in text_lower for x in ["ja", "yes", "bestätigen", "gerne", "ok"]):
                # Perform Reservation
                book_to_update = st.session_state.reservation_book
                new_dates = st.session_state.reservation_dates
                
                # Update in memory list
                for book in books_data:
                    if book['title'] == book_to_update['title']:
                        # Update available_from to end_date (assuming it's blocked until then)
                        # Or maybe available_from should be the next day after reservation?
                        # The prompt says: "Dauer von 3 Tagen".
                        # Let's set available_from to end_date.
                        book['available_from'] = new_dates['end'].strftime("%Y-%m-%d")
                        break
                
                # Save to file
                save_json(books_file, books_data)
                
                msg = random.choice(dialogue_flow['success']).format(
                    title=book_to_update['title'],
                    start_date=new_dates['start'].strftime("%d.%m.%Y"),
                    end_date=new_dates['end'].strftime("%d.%m.%Y")
                )
                st.session_state.messages.append({"role": "assistant", "content": msg})
                if used_mic:
                    st.session_state.audio_to_play = msg
                
                # End flow
                st.session_state.reservation_step = None
                st.session_state.current_flow = None
                st.session_state.reservation_book = None
                
            elif any(x in text_lower for x in ["nein", "no", "abbruch", "nicht"]):
                msg = random.choice(dialogue_flow['cancel'])
                st.session_state.messages.append({"role": "assistant", "content": msg})
                if used_mic:
                    st.session_state.audio_to_play = msg
                
                # End flow
                st.session_state.reservation_step = None
                st.session_state.current_flow = None
                st.session_state.reservation_book = None
            else:
                # Unclear response
                msg = random.choice(dialogue_flow['clarify_confirmation'])
                st.session_state.messages.append({"role": "assistant", "content": msg})
                if used_mic:
                    st.session_state.audio_to_play = msg