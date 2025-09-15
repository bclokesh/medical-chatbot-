import os
from flask import Flask, render_template, request
from medical_data import get_medical_info, format_medical_response

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
    
    # Get medical information based on the query
    medical_info = get_medical_info(user_input)
    
    if medical_info:
        response = format_medical_response(medical_info)
    else:
        # General medical advice for unrecognized queries
        response = f"""I understand you're asking about: "{user_input}"

I have information about common medical conditions and WHO-verified medicines including:

**Medical Conditions:**
• Flu and cold symptoms
• Fever and headaches
• Cough and sore throat
• Diabetes and high blood pressure

**WHO-Verified Medicines:**
• Pain relievers: Tylenol, Advil, Aspirin
• Cold/flu medicines: Tamiflu, Sudafed, Robitussin
• Allergy medicines: Claritin, Zyrtec
• Diabetes medicines: Metformin, Insulin
• Blood pressure medicines: Lisinopril, Norvasc

Try asking:
- "What are the symptoms of flu?"
- "Tell me about Tylenol"
- "How to treat a fever?"
- "What is Metformin used for?"

⚠️ **Important:** This is for educational purposes only. Always consult with a healthcare professional for proper medical advice and diagnosis."""

    print(f"Response: {response}")
    return str(response)

if __name__ == '__main__':
    # Run without debug mode to avoid dotenv issues
    app.run(host="127.0.0.1", port=8080, debug=False)
