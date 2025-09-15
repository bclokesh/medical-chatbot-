#!/usr/bin/env python3
"""
Simple voice test script to diagnose TTS issues
"""
import pyttsx3
import time

def test_voice():
    print("Testing Text-to-Speech functionality...")
    
    try:
        # Initialize TTS engine
        engine = pyttsx3.init()
        print("✅ TTS engine initialized successfully")
        
        # Get available voices
        voices = engine.getProperty('voices')
        print(f"✅ Found {len(voices)} available voices:")
        for i, voice in enumerate(voices):
            print(f"   {i+1}. {voice.name} (ID: {voice.id})")
        
        # Set voice properties
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        
        if voices:
            engine.setProperty('voice', voices[0].id)
            print(f"✅ Using voice: {voices[0].name}")
        
        # Test 1: Simple message
        print("\n🔊 Test 1: Saying 'Hello, this is a test'")
        engine.say("Hello, this is a test")
        engine.runAndWait()
        print("✅ Test 1 completed")
        
        # Test 2: Medical message
        print("\n🔊 Test 2: Saying medical information")
        medical_text = "This is a test of the medical voice assistant. The system is working correctly."
        engine.say(medical_text)
        engine.runAndWait()
        print("✅ Test 2 completed")
        
        # Test 3: Check if audio is working
        print("\n🔊 Test 3: Volume and clarity test")
        engine.say("If you can hear this message clearly, the voice system is working properly.")
        engine.runAndWait()
        print("✅ Test 3 completed")
        
        print("\n🎉 All voice tests completed successfully!")
        print("If you didn't hear any audio, check:")
        print("1. Your computer's volume is turned up")
        print("2. Your speakers/headphones are connected")
        print("3. Windows audio is not muted")
        print("4. No other applications are blocking audio")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_voice()
