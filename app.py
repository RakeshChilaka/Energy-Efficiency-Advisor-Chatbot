from flask import Flask, render_template, request, jsonify
import random
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer
from utils.knowledgebase import knowledge_base
from utils.intent_keywords import intent_keywords

# Initialize NLTK components
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()
tokenizer = TreebankWordTokenizer()

app = Flask(__name__)
conversation_state = {"expecting_appliance": False}

def preprocess_text(text):
    tokens = tokenizer.tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalnum() and word not in stop_words]
    return tokens


def identify_intent(user_input):
    tokens = preprocess_text(user_input)
    
    # Check for specific appliance-related intents first
    for intent, keywords in intent_keywords.items():
        if intent != "energy_saving" and any(keyword in user_input.lower() for keyword in keywords):
            return intent
    
    # If no specific appliance intent is found, check for general intents
    if any(keyword in user_input.lower() for keyword in intent_keywords["energy_saving"]):
        return "energy_saving"
    
    return "unknown"

def generate_response(intent):
    if intent == "appliance_selection":
        conversation_state["expecting_appliance"] = True
        return "Which appliance would you like to save energy on? Here are some options,Choose a required one."
    elif intent in knowledge_base:
        conversation_state["expecting_appliance"] = False
        return random.choice(knowledge_base[intent])
    else:
        conversation_state["expecting_appliance"] = False
        return "I'm sorry, I don't have information on that. Could you ask something else?"

@app.route("/")
def home():
    return render_template("home.html")

# Route for the chatbot interface (index page)
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("message")
    if conversation_state["expecting_appliance"]:
        # Handle appliance-specific tips request
        appliance_intent = identify_intent(user_input)
        if appliance_intent in knowledge_base:
            response = generate_response(appliance_intent)
            conversation_state["expecting_appliance"] = False  # Reset state after responding
        else:
            response = "Please select a valid appliance: Air Conditioner, Refrigerator."
    else:
        # Handle general inquiries
        general_intent = identify_intent(user_input)
        response = generate_response(general_intent)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
