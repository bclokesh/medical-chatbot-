#!/usr/bin/env python3
"""
Simple Medical Assistant with Camera Feature (No OCR dependencies)
"""
import os
import base64
import io
from flask import Flask, render_template, request, jsonify
from medical_data import get_medical_info, format_medical_response
import subprocess
import threading

# Initialize Flask App
app = Flask(__name__)

# Set API Keys directly
os.environ['GOOGLE_API_KEY'] = "AIzaSyCR6NXeebzPPbmMmFWVQAZlXRq-JLL77Gg"
os.environ['PINECONE_API_KEY'] = "pcsk_2tXJEi_9oife2zxXQBKbPhqU9apc2M9Ai2h7Js8dMV4LyhKTHzVaebffuK38kEwN7BWeu7a"

def speak_with_sapi(text):
    """Use Windows SAPI directly"""
    try:
        clean_text = text.replace('**', '').replace('•', '').replace('⚠️', 'Warning:')
        clean_text = clean_text.replace('✅', 'Approved').replace('❌', 'Not approved')
        
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
    """Convert text to speech"""
    print(f"Speaking: {text[:100]}...")
    speak_with_sapi(text)

def save_prescription_image(image_data):
    """Save prescription image for manual review"""
    try:
        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1])
        
        # Create uploads directory if it doesn't exist
        upload_dir = 'uploads'
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        # Save image with timestamp
        import time
        timestamp = int(time.time())
        filename = f"prescription_{timestamp}.jpg"
        filepath = os.path.join(upload_dir, filename)
        
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        
        return filepath
        
    except Exception as e:
        print(f"Error saving image: {e}")
        return None

def generate_prescription_analysis():
    """Generate a sample prescription analysis"""
    return """**📋 Prescription Analysis**


*

@app.route("/")
def index():
    return render_template('simple_camera_chat.html')

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

Or use the camera to scan a prescription!

⚠️ **Important:** This is for educational purposes only. Always consult with a healthcare professional for proper medical advice and diagnosis."""

    print(f"Response: {response}")
    return str(response)

@app.route("/process-prescription", methods=["POST"])
def process_prescription():
    """Process prescription image"""
    try:
        data = request.get_json()
        image_data = data.get('image', '')
        
        if not image_data:
            return jsonify({"success": False, "error": "No image data provided"})
        
        print("Processing prescription image...")
        
        # Save the image
        filepath = save_prescription_image(image_data)
        
        if filepath:
            print(f"Prescription image saved: {filepath}")
            
            # Generate analysis response
            response = generate_prescription_analysis()
            
            return jsonify({
                "success": True,
                "response": response,
                "image_saved": filepath,
                "message": "Prescription image captured and saved successfully!"
            })
        else:
            return jsonify({
                "success": False, 
                "error": "Could not save prescription image."
            })
        
    except Exception as e:
        print(f"Prescription processing error: {e}")
        return jsonify({"success": False, "error": str(e)})

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
        test_message = "Camera and voice features are ready. You can now scan prescriptions and hear responses."
        tts_thread = threading.Thread(target=speak_text, args=(test_message,))
        tts_thread.daemon = True
        tts_thread.start()
        return jsonify({"success": True, "message": "Voice test started"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    print("Starting Simple Medical Assistant with Camera...")
    print("Features: Voice output, Camera capture, Image saving, Medical knowledge")
    
    # Test voice on startup
    try:
        test_message = "Medical assistant with camera features ready. You can now scan prescriptions and ask medical questions."
        speak_text(test_message)
    except:
        print("Startup voice test failed, but continuing...")
    
    app.run(host="127.0.0.1", port=8080, debug=False)
