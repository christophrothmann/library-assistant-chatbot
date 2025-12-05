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
nltk.download('punkt_tab', quiet=True, raise_on_error=True)

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
import os

def load_training_data():
    file_path = os.path.join("assets", "training_data.json")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

training_data = load_training_data()

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

