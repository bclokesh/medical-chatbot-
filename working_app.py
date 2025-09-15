import os
from flask import Flask, render_template, request

# Initialize Flask App
app = Flask(__name__)

# Set API Keys directly (bypassing .env file issues)
os.environ['GOOGLE_API_KEY'] = "AIzaSyCR6NXeebzPPbmMmFWVQAZlXRq-JLL77Gg"
os.environ['PINECONE_API_KEY'] = "pcsk_2tXJEi_9oife2zxXQBKbPhqU9apc2M9Ai2h7Js8dMV4LyhKTHzVaebffuK38kEwN7BWeu7a"

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    user_input = msg
    print(f"User Input: {user_input}")
    
    # Simple response for now
    response = f"I received your message: '{user_input}'. The medical chatbot is running! For full AI functionality, the vector database needs to be set up with medical knowledge."
    
    print(f"Response: {response}")
    return str(response)

if __name__ == '__main__':
    # Run without debug mode to avoid dotenv issues
    app.run(host="127.0.0.1", port=8080, debug=False)

