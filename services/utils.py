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
