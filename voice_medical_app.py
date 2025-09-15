import os
import speech_recognition as sr
import pyttsx3
from flask import Flask, render_template, request, jsonify
from medical_data import get_medical_info, format_medical_response
import threading
import time

# Initialize Flask App
app = Flask(__name__)

# Set API Keys directly
os.environ['GOOGLE_API_KEY'] = "AIzaSyCR6NXeebzPPbmMmFWVQAZlXRq-JLL77Gg"
os.environ['PINECONE_API_KEY'] = "pcsk_2tXJEi_9oife2zxXQBKbPhqU9apc2M9Ai2h7Js8dMV4LyhKTHzVaebffuK38kEwN7BWeu7a"

# Initialize speech recognition and text-to-speech
recognizer = sr.Recognizer()
microphone = sr.Microphone()
tts_engine = pyttsx3.init()

# Configure TTS
tts_engine.setProperty('rate', 150)  # Speed of speech
tts_engine.setProperty('volume', 0.8)  # Volume level

def speak_text(text):
    """Convert text to speech"""
    try:
        # Clean text for better speech
        clean_text = text.replace('**', '').replace('•', '').replace('⚠️', 'Warning:')
        tts_engine.say(clean_text)
        tts_engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")

def listen_for_speech():
    """Listen for speech input and return transcribed text"""
    try:
        with microphone as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        
        print("Processing speech...")
        text = recognizer.recognize_google(audio)
        print(f"Recognized: {text}")
        return text
    except sr.WaitTimeoutError:
        return "No speech detected"
    except sr.UnknownValueError:
        return "Could not understand speech"
    except Exception as e:
        print(f"Speech recognition error: {e}")
        return "Speech recognition error"

@app.route("/")
def index():
    return render_template('voice_chat.html')

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

@app.route("/voice_input", methods=["POST"])
def voice_input():
    """Handle voice input"""
    try:
        # Listen for speech
        text = listen_for_speech()
        
        if text in ["No speech detected", "Could not understand speech", "Speech recognition error"]:
            return jsonify({"success": False, "text": text})
        
        # Get medical response
        medical_info = get_medical_info(text)
        
        if medical_info:
            response = format_medical_response(medical_info)
        else:
            response = f"I heard: '{text}'. Could you please be more specific about your medical question?"
        
        return jsonify({"success": True, "text": text, "response": response})
    
    except Exception as e:
        return jsonify({"success": False, "text": f"Error: {str(e)}"})

@app.route("/speak", methods=["POST"])
def speak():
    """Handle text-to-speech"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        # Start TTS in a separate thread to avoid blocking
        tts_thread = threading.Thread(target=speak_text, args=(text,))
        tts_thread.start()
        
        return jsonify({"success": True})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    # Test microphone and TTS on startup
    print("Initializing voice assistant...")
    try:
        # Test TTS
        speak_text("Voice assistant ready. How can I help you with your medical questions?")
        print("Voice assistant initialized successfully!")
    except Exception as e:
        print(f"Voice initialization error: {e}")
    
    app.run(host="127.0.0.1", port=8080, debug=False)

