import os
from flask import Flask, render_template, request, jsonify
from medical_data import get_medical_info, format_medical_response
import pyttsx3
import threading

# Initialize Flask App
app = Flask(__name__)

# Set API Keys directly
os.environ['GOOGLE_API_KEY'] = "AIzaSyCR6NXeebzPPbmMmFWVQAZlXRq-JLL77Gg"
os.environ['PINECONE_API_KEY'] = "pcsk_2tXJEi_9oife2zxXQBKbPhqU9apc2M9Ai2h7Js8dMV4LyhKTHzVaebffuK38kEwN7BWeu7a"

# Initialize text-to-speech
try:
    tts_engine = pyttsx3.init()
    tts_engine.setProperty('rate', 150)
    tts_engine.setProperty('volume', 1.0)  # Maximum volume
    # Set a specific voice for better compatibility
    voices = tts_engine.getProperty('voices')
    if voices:
        tts_engine.setProperty('voice', voices[0].id)  # Use first available voice
    tts_available = True
    print(f"TTS initialized with voice: {voices[0].name if voices else 'Default'}")
except Exception as e:
    print(f"TTS initialization failed: {e}")
    tts_available = False

def speak_text(text):
    """Convert text to speech"""
    if not tts_available:
        print("TTS not available")
        return
    try:
        # Clean text for better speech
        clean_text = text.replace('**', '').replace('•', '').replace('⚠️', 'Warning:')
        clean_text = clean_text.replace('✅', 'Approved').replace('❌', 'Not approved')
        print(f"Speaking: {clean_text[:100]}...")
        
        # Test with a simple message first
        test_message = "Hello, this is a test of the voice system."
        tts_engine.say(test_message)
        tts_engine.runAndWait()
        print("Test message completed")
        
        # Now speak the actual content
        tts_engine.say(clean_text)
        tts_engine.runAndWait()
        print("TTS completed successfully")
    except Exception as e:
        print(f"TTS Error: {e}")

@app.route("/")
def index():
    return render_template('simple_voice_chat.html')

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

@app.route("/speak", methods=["POST"])
def speak():
    """Handle text-to-speech"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        print(f"Received TTS request: {text[:50]}...")
        
        if tts_available:
            # Start TTS in a separate thread to avoid blocking
            tts_thread = threading.Thread(target=speak_text, args=(text,))
            tts_thread.daemon = True
            tts_thread.start()
            print("TTS thread started")
            return jsonify({"success": True, "tts_available": True})
        else:
            print("TTS not available")
            return jsonify({"success": False, "tts_available": False, "error": "TTS not available"})
    
    except Exception as e:
        print(f"TTS endpoint error: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route("/test-voice", methods=["GET"])
def test_voice():
    """Test voice functionality"""
    try:
        if tts_available:
            test_message = "Voice test successful. The medical assistant is ready to help you."
            tts_thread = threading.Thread(target=speak_text, args=(test_message,))
            tts_thread.daemon = True
            tts_thread.start()
            return jsonify({"success": True, "message": "Voice test started"})
        else:
            return jsonify({"success": False, "error": "TTS not available"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    print("Starting Medical Voice Assistant...")
    if tts_available:
        print("Text-to-Speech: Available")
        # Test TTS
        try:
            speak_text("Medical voice assistant ready. How can I help you with your medical questions?")
        except:
            print("TTS test failed, but continuing...")
    else:
        print("Text-to-Speech: Not available")
    
    app.run(host="127.0.0.1", port=8080, debug=False)

