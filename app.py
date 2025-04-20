from flask import Flask, render_template, request, jsonify
import random
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer
from utils.knowledgebase import knowledge_base
from utils.intent_keywords import intent_keywords

# NLTK setup
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()
tokenizer = TreebankWordTokenizer()

app = Flask(__name__)

conversation_state = {
    "expecting_appliance": False,
    "energy_saving_count": 0,
    "appliance_selection_done": False
}

def preprocess_text(text):
    tokens = tokenizer.tokenize(text.lower())
    return [lemmatizer.lemmatize(word) for word in tokens if word.isalnum() and word not in stop_words]

def identify_intents(user_input):
    tokens = preprocess_text(user_input)
    detected_intents = []

    for intent, keywords in intent_keywords.items():
        if any(keyword.lower() in user_input.lower() for keyword in keywords):
            detected_intents.append(intent)

    return list(set(detected_intents))

def generate_combined_response(intents):
    responses = []
    for intent in intents:
        if intent in knowledge_base:
            responses.append(random.choice(knowledge_base[intent]))
    return " ".join(responses)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("message")
    intents = identify_intents(user_input)
    show_appliance_options = False

    # Check if appliance is directly selected
    if "appliance_selection" in intents and not conversation_state["appliance_selection_done"]:
        matched_appliance = None
        for keyword in intent_keywords["appliance_selection"]:
            if keyword.lower() in user_input.lower():
                matched_appliance = keyword
                break

        if matched_appliance:
            # conversation_state["expecting_appliance"] = False
            conversation_state["appliance_selection_done"] = True
            conversation_state["expecting_appliance"] = False
            show_appliance_options = True
            return jsonify({
                "response": "Which appliance would you like to save energy on? Here are some options:",
                "show_appliance_options": True
            })
        
        conversation_state["appliance_selection_done"] = False
        conversation_state["expecting_appliance"] = True
    if "energy_saving" in intents:
        conversation_state["energy_saving_count"] += 1

    # Ask for appliance if energy_saving mentioned enough times
    if (conversation_state["energy_saving_count"] > 1):
        conversation_state["expecting_appliance"] = True
        show_appliance_options = True
        conversation_state["energy_saving_count"] = 0
        return jsonify({
            "response": "Which appliance would you like to save energy on? Here are some options:",
            "show_appliance_options": True
        })

    if conversation_state.get("expecting_appliance"):
        matched_appliance = None
        for keyword in intent_keywords["appliance_selection"]:
            if keyword.lower() in user_input.lower():
                matched_appliance = keyword
                break

        if matched_appliance:
            conversation_state["expecting_appliance"] = False
            conversation_state["appliance_selection_done"] = True
            return jsonify({
                "response": generate_combined_response(matched_appliance),
                "show_appliance_options": False
            })
    if intents:
        response_text = generate_combined_response(intents)
    else:
        response_text = "I'm sorry, I couldn't understand. Can you try rephrasing?"

    return jsonify({"response": response_text, "show_appliance_options": False})
if __name__ == "__main__":
    app.run(debug=True, port=5001)
