#!/usr/bin/env python3
"""
Medical Assistant with Camera and Prescription Recognition
"""
import os
import cv2
import base64
import io
import re
from flask import Flask, render_template, request, jsonify
from medical_data import get_medical_info, format_medical_response
import subprocess
import threading
from PIL import Image
import pytesseract
import numpy as np

# Initialize Flask App
app = Flask(__name__)

# Set API Keys directly
os.environ['GOOGLE_API_KEY'] = "AIzaSyCR6NXeebzPPbmMmFWVQAZlXRq-JLL77Gg"
os.environ['PINECONE_API_KEY'] = "pcsk_2tXJEi_9oife2zxXQBKbPhqU9apc2M9Ai2h7Js8dMV4LyhKTHzVaebffuK38kEwN7BWeu7a"

# Configure Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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

def preprocess_image(image):
    """Preprocess image for better OCR"""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply threshold to get binary image
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Morphological operations to clean up the image
    kernel = np.ones((1, 1), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    return cleaned

def extract_text_from_image(image_data):
    """Extract text from image using OCR"""
    try:
        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1])
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert PIL image to OpenCV format
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Preprocess image
        processed_image = preprocess_image(opencv_image)
        
        # Extract text using Tesseract
        text = pytesseract.image_to_string(processed_image, config='--psm 6')
        
        return text.strip()
        
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""

def parse_prescription(text):
    """Parse prescription text to extract structured information"""
    prescription_data = {
        "patient_name": "",
        "doctor_name": "",
        "date": "",
        "diagnosis": "",
        "medicines": [],
        "raw_text": text
    }
    
    # Extract patient name (look for patterns like "Patient:", "Name:", etc.)
    patient_patterns = [
        r'Patient[:\s]+([A-Za-z\s]+)',
        r'Name[:\s]+([A-Za-z\s]+)',
        r'Patient Name[:\s]+([A-Za-z\s]+)'
    ]
    
    for pattern in patient_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            prescription_data["patient_name"] = match.group(1).strip()
            break
    
    # Extract doctor name
    doctor_patterns = [
        r'Dr[.\s]+([A-Za-z\s]+)',
        r'Doctor[:\s]+([A-Za-z\s]+)',
        r'Physician[:\s]+([A-Za-z\s]+)'
    ]
    
    for pattern in doctor_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            prescription_data["doctor_name"] = match.group(1).strip()
            break
    
    # Extract date
    date_patterns = [
        r'Date[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            prescription_data["date"] = match.group(1)
            break
    
    # Extract diagnosis
    diagnosis_patterns = [
        r'Diagnosis[:\s]+([A-Za-z\s,]+?)(?:\n|Medication|Rx|Prescription)',
        r'Condition[:\s]+([A-Za-z\s,]+?)(?:\n|Medication|Rx|Prescription)',
        r'Problem[:\s]+([A-Za-z\s,]+?)(?:\n|Medication|Rx|Prescription)'
    ]
    
    for pattern in diagnosis_patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            prescription_data["diagnosis"] = match.group(1).strip()
            break
    
    # Extract medicines (look for common medicine patterns)
    medicine_patterns = [
        r'([A-Za-z]+(?:\s+[A-Za-z]+)*)\s+(\d+\s*mg?)\s+([A-Za-z\s\d,]+)',
        r'Rx[:\s]+([A-Za-z\s]+?)(?:\n|$)',
        r'Medication[:\s]+([A-Za-z\s]+?)(?:\n|$)'
    ]
    
    for pattern in medicine_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                medicine = {
                    "name": match[0].strip(),
                    "dosage": match[1].strip() if len(match) > 1 else "",
                    "instructions": match[2].strip() if len(match) > 2 else ""
                }
            else:
                medicine = {
                    "name": match.strip(),
                    "dosage": "",
                    "instructions": ""
                }
            prescription_data["medicines"].append(medicine)
    
    return prescription_data

def format_prescription_response(prescription_data):
    """Format prescription data into a readable response"""
    response = "**📋 Prescription Analysis**\n\n"
    
    if prescription_data["patient_name"]:
        response += f"**Patient:** {prescription_data['patient_name']}\n"
    
    if prescription_data["doctor_name"]:
        response += f"**Doctor:** {prescription_data['doctor_name']}\n"
    
    if prescription_data["date"]:
        response += f"**Date:** {prescription_data['date']}\n"
    
    if prescription_data["diagnosis"]:
        response += f"**Diagnosis:** {prescription_data['diagnosis']}\n"
    
    if prescription_data["medicines"]:
        response += "\n**💊 Prescribed Medicines:**\n"
        for i, medicine in enumerate(prescription_data["medicines"], 1):
            response += f"{i}. **{medicine['name']}**"
            if medicine['dosage']:
                response += f" - {medicine['dosage']}"
            if medicine['instructions']:
                response += f"\n   Instructions: {medicine['instructions']}"
            response += "\n"
    
    response += "\n**📝 Raw Text Extracted:**\n"
    response += prescription_data["raw_text"][:500] + "..." if len(prescription_data["raw_text"]) > 500 else prescription_data["raw_text"]
    
    response += "\n\n⚠️ **Important:** This is an automated analysis. Always verify with your healthcare provider."
    
    return response

@app.route("/")
def index():
    return render_template('camera_medical_chat.html')

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
    """Process prescription image and extract information"""
    try:
        data = request.get_json()
        image_data = data.get('image', '')
        
        if not image_data:
            return jsonify({"success": False, "error": "No image data provided"})
        
        print("Processing prescription image...")
        
        # Extract text from image
        extracted_text = extract_text_from_image(image_data)
        
        if not extracted_text:
            return jsonify({
                "success": False, 
                "error": "Could not extract text from image. Please ensure the image is clear and readable."
            })
        
        # Parse prescription
        prescription_data = parse_prescription(extracted_text)
        
        # Format response
        response = format_prescription_response(prescription_data)
        
        return jsonify({
            "success": True,
            "response": response,
            "prescription_data": prescription_data
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
    print("Starting Medical Assistant with Camera and Prescription Recognition...")
    print("Features: Voice output, Camera capture, OCR, Prescription analysis")
    
    # Test voice on startup
    try:
        test_message = "Medical assistant with camera features ready. You can now scan prescriptions and ask medical questions."
        speak_text(test_message)
    except:
        print("Startup voice test failed, but continuing...")
    
    app.run(host="127.0.0.1", port=8080, debug=False)
