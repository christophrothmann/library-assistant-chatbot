import random
import nltk
from nltk.tokenize import word_tokenize
from collections import defaultdict
import json
#  sas-07-intent-classifier.py

# Notiz von mir:
# Das Skript mappt die aufgenommene Sprache in Textform auf die Intents (Aktionen)

# Download the 'punkt' tokenizer model (if you haven't already)
nltk.download('punkt', quiet=True, raise_on_error=True)

def extract_features(text):
    """
    Converts a text string into a Bag-of-Words feature dictionary.
    """
    features = {}
    # Tokenize the text into a list of words
    words = word_tokenize(text.lower())
    
    # Create a feature for the presence of each word
    for word in words:
        features[f'has({word})'] = True
    
    return features

# Our training data for a simple Mensa Assistant
# from example dialogs!
training_data = [
    # Use Case 1: Verfügbarkeit prüfen
    ("Verfügbarkeit Kauffman - Werbepsychologie", "verfuegbarkeit_pruefen"),
    ("Hallo Goleo. Ich suche ein Buch für meine Hausarbeit in Maschinenbau. Kannst du schauen, ob es da ist?", "verfuegbarkeit_pruefen"),
    ("Dubbel", "verfuegbarkeit_pruefen"),
    ("Ist Sozialpsychologie von Aronson in der 6. Auflage da?", "verfuegbarkeit_pruefen"),
    ("Ich suche Technische Mechnik 1", "verfuegbarkeit_pruefen"),
    ("Gibt es das Mathe-Buch von Papula noch?", "verfuegbarkeit_pruefen"),

    # Use Case 2: Buch Reservierung
    ("Konsumentenverhalten von Kroeber-Riel", "reservieren"),
    ("Ich brauche das Physik-Buch von Tipler", "reservieren"),
    ("Kann ich den Bortz - Statistik ab morgen für 3 Tage haben?", "reservieren"),
    ("Kostet das Reservieren von Büchern Geld?", "reservieren"),
    ("Dann bitte Werkstoffkunde von Bargel", "reservieren"),
    ("Storniere meine Reservierung für Wirtschaftsinformatik", "reservieren"),

    # Use Case 3: Regalsuche
    ("Ich bin gerade in der Bibliothek, aber ich finde das Regal für Maschinenbau nicht", "regalsuche"),
    ("Ich suche den Hering", "regalsuche"),
    ("Wo steht Psychologie von Zimbardo?", "regalsuche"),
    ("Standorte für: Kostenrechnung (Coenenberg) und Bilanzierung (Baetge)", "regalsuche"),

    # Use Case 4: Buchsuche (Inhalt & Thema)
    ("Welches Buch enthält aktuelle Definitionen zu Nudging im Kontext Marketing?", "buchsuche"),
    ("Ich muss eine Arbeit über Getriebe schreiben. Welche Bücher sind da gut für Anfänger?", "buchsuche"),
    ("Ich suche was über Metalle und so", "buchsuche"),
    ("Eher für Maschinenbau. Wie hart die sind und so", "buchsuche"),
    ("In welchem Buch finde ich das 4-Ohren-Modell?", "buchsuche")
]

# Global variable to store the trained classifier
_classifier = None

def train_classifier():
    """
    Trains the Naive Bayes Classifier using the global training_data.
    Returns the trained classifier.
    """
    global _classifier
    if _classifier:
        return _classifier

    # Create the feature sets
    feature_sets = [
        (extract_features(utterance), intent) 
        for (utterance, intent) in training_data
    ]
    
    # Shuffle the feature sets for good measure
    random.shuffle(feature_sets)
    
    # Train the Naive Bayes Classifier
    _classifier = nltk.NaiveBayesClassifier.train(feature_sets)
    return _classifier

def classify_intent(text):
    """
    Classifies the intent of the given text.
    Returns the intent label (function name).
    """
    classifier = train_classifier()
    features = extract_features(text)
    classification = classifier.classify(features)
    return classification

