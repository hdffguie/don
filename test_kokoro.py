import os
import urllib.request
import soundfile as sf
from kokoro_onnx import Kokoro
import sys

def download_file(url, filename):
    if not os.path.exists(filename):
        print(f"📥 Downloading {filename} (Please wait)...")
        urllib.request.urlretrieve(url, filename)
        print(f"✅ {filename} downloaded successfully!")

def test_kokoro_voice():
    print("⚙️ Setting up Kokoro...")
    try:
        # HuggingFace ki jagah direct official releases se ONNX format download kar rahe hain
        download_file("https://github.com/thewh1teagle/kokoro-onnx/releases/download/model/kokoro-v0_19.onnx", "kokoro-v0_19.onnx")
        download_file("https://github.com/thewh1teagle/kokoro-onnx/releases/download/model/voices.json", "voices.json")
        
        # Load the model
        kokoro = Kokoro("kokoro-v0_19.onnx", "voices.json")
        print("✅ Model Loaded Successfully on GitHub CPU!")
    except Exception as e:
        print(f"❌ Model Download/Load Failed: {e}")
        sys.exit(1)

    # Text jo hume test karna hai
    text = "Guys, YouTube automation se earning karna bahut easy hai. Smart log apna time waste nahi karte. DM me GROW to start now."
    output_file = "kokoro_test_voice.wav"

    print(f"⏳ Generating Voice for: '{text}'...")
    
    try:
        # 'am_adam' ek deep American Male voice hai.
        samples, sample_rate = kokoro.create(
            text, 
            voice="am_adam", 
            speed=1.0, 
            lang="en-us"
        )
        
        # Audio ko save karna
        sf.write(output_file, samples, sample_rate)
        print(f"✅ BOOM! Kokoro Voice successfully generated: {output_file}")
        
    except Exception as e:
        print(f"❌ Voice Generation Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_kokoro_voice()
