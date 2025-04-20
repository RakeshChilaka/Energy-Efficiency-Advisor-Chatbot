# Install required libraries
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.tokenize import TreebankWordTokenizer

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import random
import json
import re
# Sample knowledge base for intents and responses
knowledge_base = {
    "energy_saving_tips": [
        "Use LED bulbs instead of incandescent ones to save energy.",
        "Turn off appliances when not in use to reduce standby power consumption.",
        "Use a programmable thermostat to control heating and cooling efficiently."
    ],
    "air_conditioner_tips": [
        "Clean or replace your AC filter regularly to improve efficiency.",
        "Set the temperature to 24°C or higher for optimal energy savings.",
        "Ensure that doors and windows are closed when the AC is on to save energy."
    ],
    "refrigerator_tips": [
        "Keep the refrigerator away from heat sources like ovens and direct sunlight.",
        "Don't overload the fridge to ensure good air circulation inside.",
        "Set the refrigerator temperature between 3-5°C for optimal efficiency."
    ]
}


# Initialize stopwords and lemmatizer
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()
tokenizer = TreebankWordTokenizer()

def preprocess_text(text):
    tokens = tokenizer.tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalnum() and word not in stop_words]
    return tokens
# Define keywords for each intent
intent_keywords = {
    "energy_saving_tips": ["save energy", "reduce energy", "lower electricity"],
    "air_conditioner_tips": ["air conditioner", "ac", "cooling"],
    "refrigerator_tips": ["fridge", "refrigerator", "cold"]
}

def identify_intent(user_input):
    # Preprocess user input
    tokens = preprocess_text(user_input)
    for intent, keywords in intent_keywords.items():
        if any(keyword in tokens for keyword in keywords):
            return intent
    return "unknown"
def generate_response(intent):
    if intent in knowledge_base:
        return random.choice(knowledge_base[intent])
    else:
        return "I'm sorry, I don't have information on that. Could you ask something else?"
def chatbot():
    print("Hello! I'm your Energy Efficiency Advisor. Ask me about saving energy!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye! Stay energy-efficient!")
            break
        # Identify the intent
        intent = identify_intent(user_input)
        # Generate a response
        response = generate_response(intent)
        print(f"Chatbot: {response}")
chatbot()
