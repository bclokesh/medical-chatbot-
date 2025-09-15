import os
from flask import Flask, render_template, jsonify, request

# Initialize Flask App
app = Flask(__name__)

# Disable dotenv loading to avoid encoding issues
app.config['LOAD_DOTENV'] = False

# Set API Keys from environment variables
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

# --- Flask Routes ---

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    user_input = msg
    print(f"User Input: {user_input}")
    
    # Simple response for now
    response = f"I received your message: '{user_input}'. The full medical chatbot functionality requires the vector database to be set up first. Please run 'python store_index.py' to populate the Pinecone database with medical knowledge."
    
    print(f"Response: {response}")
    return str(response)

# --- Main Execution ---

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
