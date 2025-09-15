#!/usr/bin/env python3
"""
Working Voice Medical Assistant - Alternative approach
"""
import os
from flask import Flask, render_template, request, jsonify
from medical_data import get_medical_info, format_medical_response
import subprocess
import threading

# Initialize Flask App
app = Flask(__name__)

# Set API Keys directly
os.environ['GOOGLE_API_KEY'] = "AIzaSyCR6NXeebzPPbmMmFWVQAZlXRq-JLL77Gg"
os.environ['PINECONE_API_KEY'] = "pcsk_2tXJEi_9oife2zxXQBKbPhqU9apc2M9Ai2h7Js8dMV4LyhKTHzVaebffuK38kEwN7BWeu7a"

def speak_with_powershell(text):
    """Use PowerShell to speak text - more reliable on Windows"""
    try:
        # Clean text for better speech
        clean_text = text.replace('**', '').replace('•', '').replace('⚠️', 'Warning:')
        clean_text = clean_text.replace('✅', 'Approved').replace('❌', 'Not approved')
        
        # Escape quotes for PowerShell
        clean_text = clean_text.replace('"', '""')
        
        # Use PowerShell Add-Type to create speech synthesis
        ps_command = f'''
        Add-Type -AssemblyName System.Speech
        $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
        $speak.Volume = 100
        $speak.Rate = 0
        $speak.Speak("{clean_text}")
        '''
        
        # Execute PowerShell command
        subprocess.run(['powershell', '-Command', ps_command], 
                      capture_output=True, text=True, timeout=30)
        print("PowerShell TTS completed successfully")
        return True
        
    except Exception as e:
        print(f"PowerShell TTS Error: {e}")
        return False

def speak_with_sapi(text):
    """Use Windows SAPI directly"""
    try:
        clean_text = text.replace('**', '').replace('•', '').replace('⚠️', 'Warning:')
        clean_text = clean_text.replace('✅', 'Approved').replace('❌', 'Not approved')
        
        # Use Windows SAPI via COM
        import win32com.client
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Volume = 100
        speaker.Rate = 0
        speaker.Speak(clean_text)
        print("SAPI TTS completed successfully")
        return True
        
    except Exception as e:
        print(f"SAPI TTS Error: {e}")
        return False

def speak_text(text):
    """Try multiple TTS methods"""
    print(f"Speaking: {text[:100]}...")
    
    # Try SAPI first (most reliable)
    if speak_with_sapi(text):
        return True
    
    # Fallback to PowerShell
    if speak_with_powershell(text):
        return True
    
    print("All TTS methods failed")
    return False

@app.route("/")
def index():
    return render_template('improved_voice_chat.html')

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
        
        # Start TTS in a separate thread
        tts_thread = threading.Thread(target=speak_text, args=(text,))
        tts_thread.daemon = True
        tts_thread.start()
        print("TTS thread started")
        return jsonify({"success": True, "tts_available": True})
    
    except Exception as e:
        print(f"TTS endpoint error: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route("/test-voice", methods=["GET"])
def test_voice():
    """Test voice functionality"""
    try:
        test_message = "Voice test successful. The medical assistant is ready to help you."
        tts_thread = threading.Thread(target=speak_text, args=(test_message,))
        tts_thread.daemon = True
        tts_thread.start()
        return jsonify({"success": True, "message": "Voice test started"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    print("Starting Working Medical Voice Assistant...")
    print("Using Windows SAPI and PowerShell for reliable TTS")
    
    # Test voice on startup
    try:
        test_message = "Medical voice assistant ready. How can I help you with your medical questions?"
        speak_text(test_message)
    except:
        print("Startup voice test failed, but continuing...")
    
    app.run(host="127.0.0.1", port=8080, debug=False)
