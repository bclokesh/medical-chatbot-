#!/usr/bin/env python3
"""
Comprehensive audio diagnostic script for Windows TTS
"""
import pyttsx3
import time
import os
import subprocess

def check_audio_devices():
    """Check available audio devices using Windows commands"""
    print("🔍 Checking Windows audio devices...")
    try:
        # Check default audio device
        result = subprocess.run(['powershell', '-Command', 'Get-WmiObject -Class Win32_SoundDevice | Select-Object Name, Status'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Audio devices found:")
            print(result.stdout)
        else:
            print("❌ Could not retrieve audio device info")
    except Exception as e:
        print(f"❌ Error checking audio devices: {e}")

def test_volume_levels():
    """Test different volume levels"""
    print("\n🔊 Testing different volume levels...")
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)
        
        # Test different volume levels
        for volume in [0.5, 0.8, 1.0]:
            print(f"Testing volume level: {volume}")
            engine.setProperty('volume', volume)
            engine.say(f"Testing volume level {int(volume * 100)} percent")
            engine.runAndWait()
            time.sleep(1)
            
    except Exception as e:
        print(f"❌ Volume test error: {e}")

def test_different_voices():
    """Test different available voices"""
    print("\n🎤 Testing different voices...")
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        if not voices:
            print("❌ No voices available")
            return
            
        for i, voice in enumerate(voices[:3]):  # Test first 3 voices
            print(f"Testing voice {i+1}: {voice.name}")
            engine.setProperty('voice', voice.id)
            engine.setProperty('volume', 1.0)
            engine.setProperty('rate', 150)
            engine.say(f"Hello, this is voice {i+1}. Can you hear me clearly?")
            engine.runAndWait()
            time.sleep(2)
            
    except Exception as e:
        print(f"❌ Voice test error: {e}")

def test_windows_sapi():
    """Test Windows SAPI directly"""
    print("\n🔧 Testing Windows SAPI...")
    try:
        # Try to use Windows SAPI directly
        import win32com.client
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak("Testing Windows SAPI directly. Can you hear this?")
        print("✅ Windows SAPI test completed")
    except ImportError:
        print("❌ win32com not available, trying alternative...")
        try:
            # Alternative approach
            engine = pyttsx3.init('sapi5')
            engine.say("Testing SAPI5 engine directly")
            engine.runAndWait()
            print("✅ SAPI5 test completed")
        except Exception as e:
            print(f"❌ SAPI5 test failed: {e}")
    except Exception as e:
        print(f"❌ Windows SAPI test failed: {e}")

def check_system_volume():
    """Check system volume using PowerShell"""
    print("\n📊 Checking system volume...")
    try:
        result = subprocess.run(['powershell', '-Command', 
                               'Get-WmiObject -Class Win32_SoundDevice | Select-Object Name, Status'], 
                              capture_output=True, text=True)
        print("System audio status:")
        print(result.stdout)
        
        # Check if audio service is running
        result2 = subprocess.run(['powershell', '-Command', 
                                'Get-Service -Name "AudioSrv" | Select-Object Name, Status'], 
                               capture_output=True, text=True)
        print("Audio service status:")
        print(result2.stdout)
        
    except Exception as e:
        print(f"❌ Could not check system volume: {e}")

def main():
    print("🎵 Windows Audio Diagnostic Tool")
    print("=" * 50)
    
    # Check basic TTS functionality
    print("1. Basic TTS Test")
    try:
        engine = pyttsx3.init()
        print("✅ TTS engine initialized")
        engine.say("Basic TTS test. If you can hear this, the system is working.")
        engine.runAndWait()
        print("✅ Basic TTS test completed")
    except Exception as e:
        print(f"❌ Basic TTS test failed: {e}")
        return
    
    # Run all diagnostic tests
    check_audio_devices()
    check_system_volume()
    test_different_voices()
    test_volume_levels()
    test_windows_sapi()
    
    print("\n" + "=" * 50)
    print("🎯 DIAGNOSTIC SUMMARY:")
    print("If you didn't hear any audio during these tests:")
    print("1. Check Windows volume mixer (right-click speaker icon)")
    print("2. Ensure speakers/headphones are connected and working")
    print("3. Try playing a YouTube video to test audio")
    print("4. Check Windows audio settings in Control Panel")
    print("5. Restart Windows Audio service if needed")
    print("6. Try different audio output device")

if __name__ == "__main__":
    main()
