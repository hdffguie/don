import os
import urllib.request
import subprocess
import sys

def download_file(url, filename):
    if not os.path.exists(filename):
        print(f"📥 Downloading {filename}...")
        # Browser ka natak karna (Spoofing) taaki HF block na kare
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
        try:
            with urllib.request.urlopen(req) as response, open(filename, 'wb') as out_file:
                out_file.write(response.read())
            print(f"✅ {filename} Downloaded Successfully!")
        except Exception as e:
            print(f"❌ Error downloading {filename}: {e}")
            sys.exit(1)

def download_piper_model():
    # 🔴 Fixed URL: 'main' ki jagah 'v1.0.0' use kiya hai jo kabhi delete nahi hoga
    base_url = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/hi/hi_IN/amit/medium/hi_IN-amit-medium.onnx"
    config_url = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/hi/hi_IN/amit/medium/hi_IN-amit-medium.onnx.json"
    
    download_file(base_url, "model.onnx")
    download_file(config_url, "model.onnx.json")

def generate_voice():
    # Aapki Hindi Script
    text = "दोस्तों, यूट्यूब ऑटोमेशन से पैसा कमाना बहुत आसान है। स्मार्ट लोग अपना टाइम बर्बाद नहीं करते।"
    output_file = "piper_test_voice.wav"
    
    print(f"⏳ Generating High-Quality Voice for: '{text}'...")
    
    # Text ko terminal string me convert karna
    safe_text = text.replace('"', '\\"').replace("'", "\\'")
    
    # Python ke andar bash command run karna
    cmd = f'echo "{safe_text}" | piper --model model.onnx --output_file {output_file}'
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ BOOM! Piper Voice successfully generated: {output_file}")
    except Exception as e:
        print(f"❌ Voice Generation Failed: {e}")

if __name__ == "__main__":
    download_piper_model()
    generate_voice()
