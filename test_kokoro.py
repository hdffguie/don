import soundfile as sf
from huggingface_hub import hf_hub_download
from kokoro_onnx import Kokoro
import sys

def test_kokoro_voice():
    print("📥 Downloading Kokoro AI Model (Only runs once)...")
    try:
        # Download lightweight ONNX model from Hugging Face
        model_path = hf_hub_download(repo_id="hexgrad/Kokoro-82M", filename="kokoro-v0_19.onnx")
        voices_path = hf_hub_download(repo_id="hexgrad/Kokoro-82M", filename="voices.json")
        
        # Load the model
        kokoro = Kokoro(model_path, voices_path)
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
