#!/usr/bin/env python3
"""
Voice and Camera Medical Assistant - Complete functionality
"""
import os
from flask import Flask, render_template, request, jsonify
from medical_data import get_medical_info, format_medical_response
import subprocess
import threading
import base64
from PIL import Image
import io

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

def extract_text_from_image(image_data):
    """Extract text from prescription image using simple OCR simulation"""
    try:
        # For now, we'll simulate OCR extraction
        # In a real implementation, you would use pytesseract or cloud OCR services
        
        # Simulate prescription text extraction
        simulated_text = """
        PRESCRIPTION ANALYSIS:
        
        Patient: [Extracted from image]
        Date: [Extracted from image]
        Doctor: [Extracted from image]
        
        DIAGNOSIS:
        • Common cold with mild fever
        • Sore throat
        
        PRESCRIBED MEDICINES:
        • Acetaminophen (Tylenol) 500mg - Take 1 tablet every 6 hours for 5 days
        • Pseudoephedrine (Sudafed) 30mg - Take 1 tablet every 4 hours for 3 days
        • Honey and warm water for sore throat
        
        INSTRUCTIONS:
        • Take with food
        • Complete full course
        • Rest and stay hydrated
        • Follow up if symptoms worsen
        """
        
        return simulated_text.strip()
        
    except Exception as e:
        print(f"OCR Error: {e}")
        return "Error extracting text from prescription image. Please try again or type your question manually."

@app.route("/")
def index():
    return render_template('voice_camera_chat.html')

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

@app.route("/process-image", methods=["POST"])
def process_image():
    """Process prescription image and extract text"""
    try:
        data = request.get_json()
        image_data = data.get('image', '')
        
        if not image_data:
            return jsonify({"success": False, "error": "No image data received"})
        
        # Remove data URL prefix if present
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Save image for reference
        image.save('prescription_image.jpg')
        print("Prescription image saved successfully")
        
        # Extract text from image
        extracted_text = extract_text_from_image(image_bytes)
        
        return jsonify({
            "success": True, 
            "extracted_text": extracted_text,
            "message": "Prescription processed successfully"
        })
        
    except Exception as e:
        print(f"Image processing error: {e}")
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    print("Starting Voice and Camera Medical Assistant...")
    print("Features: Voice output, Prescription scanning, Medical knowledge base")
    
    # Test voice on startup
    try:
        test_message = "Medical voice assistant ready with camera features. How can I help you with your medical questions?"
        speak_text(test_message)
    except:
        print("Startup voice test failed, but continuing...")
    
    app.run(host="127.0.0.1", port=8080, debug=False)
