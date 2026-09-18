import os
import urllib.request
import json
import soundfile as sf
from kokoro_onnx import Kokoro
import sys

def download_file(url, filename):
    if not os.path.exists(filename):
        print(f"📥 Downloading {filename} from {url}...")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(filename, 'wb') as out_file:
                out_file.write(response.read())
            print(f"✅ {filename} download complete!")
        except Exception as e:
            print(f"❌ Failed to download {filename}: {e}")
            raise e

def test_kokoro_voice():
    print("🔍 Scanning GitHub API for the latest Kokoro files...")
    api_url = "https://api.github.com/repos/thewh1teagle/kokoro-onnx/releases/tags/model"
    
    try:
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            assets = json.loads(response.read().decode()).get("assets", [])
    except Exception as e:
        print(f"❌ GitHub API Error: {e}")
        sys.exit(1)

    onnx_url, voices_url = None, None
    onnx_name, voices_name = None, None

    # Automatically find the right files, whatever the name is!
    for asset in assets:
        name = asset["name"]
        url = asset["browser_download_url"]
        
        if name.endswith(".onnx") and onnx_url is None:
            onnx_url = url
            onnx_name = name
        if name.startswith("voices") and (name.endswith(".bin") or name.endswith(".json")):
            voices_url = url
            voices_name = name

    if not onnx_url or not voices_url:
        print("❌ Could not find the model files on the server!")
        sys.exit(1)

    print(f"🎯 Target Locked! Found: {onnx_name} and {voices_name}")
    
    # Download files dynamically
    download_file(onnx_url, onnx_name)
    download_file(voices_url, voices_name)

    print("⚙️ Loading Kokoro AI...")
    try:
        kokoro = Kokoro(onnx_name, voices_name)
        print("✅ Kokoro Model Loaded Successfully!")
    except Exception as e:
        print(f"❌ Model Setup Failed: {e}")
        sys.exit(1)

    text = "Guys, YouTube automation se earning karna bahut easy hai. Smart log apna time waste nahi karte. DM me GROW to start now."
    output_file = "kokoro_test_voice.wav"

    print(f"⏳ Generating Voice for: '{text}'...")
    
    try:
        # 'af_heart' -> Ek pyari aur clear Female voice (Ye hamesha available hoti hai)
        # Male ke liye aap 'am_adam' try kar sakte ho
        samples, sample_rate = kokoro.create(
            text, 
            voice="af_heart", 
            speed=1.0, 
            lang="en-us"
        )
        
        sf.write(output_file, samples, sample_rate)
        print(f"✅ BOOM! Kokoro Voice successfully generated: {output_file}")
        
    except Exception as e:
        print(f"❌ Voice Generation Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_kokoro_voice()
