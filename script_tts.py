import os
import numpy as np
import soundfile as sf
import torch
from transformers import AutoModel

# GitHub Actions se inputs lena
hindi_text = os.getenv("HINDI_TEXT", "नमस्ते भाई!")
ref_text = os.getenv("REF_TEXT", "यह एक सैंपल टेक्स्ट है।")

print(f"--- Processing TTS ---")
print(f"Target Text: {hindi_text}")

# 1. HuggingFace se official model pull karna (ai4bharat/IndicF5)
repo_id = "ai4bharat/IndicF5"
print("Model download ho raha hai (GitHub runner par thoda samay lag sakta hai)...")
model = AutoModel.from_pretrained(repo_id, trust_remote_code=True)

# 2. GitHub environment mein bina real mic recording ke clone karne ke liye
# Hum ek blank dummy reference audio bana rahe hain, taaki workflow error na de.
# Agar aapke paas apni koi real .wav file ho, toh use repo mein push karke uska path yahan de sakte hain.
dummy_ref_path = "dummy_ref.wav"
sr = 24000
duration = 5 # 5 seconds
dummy_audio = np.zeros(sr * duration, dtype=np.float32)
sf.write(dummy_ref_path, dummy_audio, sr)

print("Hindi Audio generate ho raha hai (CPU Mode)...")

# Force CPU inference for GitHub default runners
with torch.no_grad():
    audio = model(
        text=hindi_text,
        ref_audio_path=dummy_ref_path,
        ref_text=ref_text
    )

# 3. Output ko save karna
if audio.dtype == np.int16:
    audio = audio.astype(np.float32) / 32768.0

output_filename = "hindi_output.wav"
sf.write(output_filename, np.array(audio, dtype=np.float32), samplerate=24000)
print(f"🎉 Success! Audio saved as {output_filename}")
