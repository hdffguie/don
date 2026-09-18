import os
import urllib.request
import soundfile as sf
from kokoro_onnx import Kokoro
import sys

def download_file(url, filename):
    if not os.path.exists(filename):
        print(f"📥 Downloading {filename} (Isme thoda time lagega, ~300MB file hai)...")
        try:
            # Custom Request taaki block na ho
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(filename, 'wb') as out_file:
                out_file.write(response.read())
            print(f"✅ {filename} downloaded successfully!")
        except Exception as e:
            print(f"❌ Failed to download {filename}: {e}")
            raise e

def test_kokoro_voice():
    print("⚙️ Setting up Kokoro v1.0...")
    try:
        # 🔴 Updated URLs for Kokoro Version 1.0 (100% Working)
        download_file("https://github.com/thewh1teagle/kokoro-onnx/releases/download/model/kokoro-v1.0.onnx", "kokoro-v1.0.onnx")
        download_file("https://github.com/thewh1teagle/kokoro-onnx/releases/download/model/voices-v1.0.bin", "voices-v1.0.bin")
        
        # Load the updated model
        kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
        print("✅ Kokoro v1.0 Model Loaded Successfully on GitHub CPU!")
    except Exception as e:
        print(f"❌ Model Setup Failed: {e}")
        sys.exit(1)

    # Text jo hume test karna hai (Hinglish)
    text = "Guys, YouTube automation se earning karna bahut easy hai. Smart log apna time waste nahi karte. DM me GROW to start now."
    output_file = "kokoro_test_voice.wav"

    print(f"⏳ Generating Voice for: '{text}'...")
    
    try:
        # 'am_adam' ek clear American Male voice hai
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
