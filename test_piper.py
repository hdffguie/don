import os
import urllib.request
import subprocess

def download_piper_model():
    model_url = "https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/amit/medium/hi_IN-amit-medium.onnx"
    config_url = "https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/amit/medium/hi_IN-amit-medium.onnx.json"
    
    if not os.path.exists("model.onnx"):
        print("📥 Downloading Piper Hindi Model (Only runs once)...")
        # HF direct download link, no tokens needed, 100% stable
        urllib.request.urlretrieve(model_url, "model.onnx")
        urllib.request.urlretrieve(config_url, "model.onnx.json")
        print("✅ Model Downloaded Successfully!")

def generate_voice():
    # Aapki Hindi/Hinglish Script
    text = "दोस्तों, यूट्यूब ऑटोमेशन से पैसा कमाना बहुत आसान है। स्मार्ट लोग अपना टाइम बर्बाद नहीं करते।"
    output_file = "piper_test_voice.wav"
    
    print(f"⏳ Generating High-Quality Voice for: '{text}'...")
    
    # Text ko file me save karna
    with open("text.txt", "w", encoding="utf-8") as f:
        f.write(text)
    
    # Piper command run karna
    cmd = f"cat text.txt | piper --model model.onnx --output_file {output_file}"
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ BOOM! Piper Voice successfully generated: {output_file}")
    except Exception as e:
        print(f"❌ Voice Generation Failed: {e}")

if __name__ == "__main__":
    download_piper_model()
    generate_voice()
