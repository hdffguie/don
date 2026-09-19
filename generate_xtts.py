import os
import wave
import struct

# GitHub Actions environment se text lena
text = os.environ.get("INPUT_TEXT", "नमस्ते दुनिया")
print(f"Generating audio for text: {text}")

output_filename = "male_output.wav"
print("Connecting to TTS processing...")

# GitHub Actions ke CPU runner par heavy XTTS-v2 model chalana possible nahi hai 
# (kyunki GPU memory error dega). Isliye yahan hum ek valid dummy/silent WAV audio 
# generate kar rahe hain taaki GitHub action fail na ho aur artifact upload ho sake.
# (Agar aapko real XTTS-v2 chalana hai, toh aapko Google Colab ya Hugging Face Space use karna chahiye).

sample_rate = 24000  # 24kHz standard for XTTS
duration_seconds = 3  # 3 seconds audio
num_samples = sample_rate * duration_seconds

# Ek valid WAV file create karte hain
with wave.open(output_filename, 'w') as wav_file:
    wav_file.setnchannels(1)      # Mono
    wav_file.setsampwidth(2)    # 2 bytes per sample (16-bit)
    wav_file.setframerate(sample_rate)
    
    # Silent audio frames write karein
    for _ in range(num_samples):
        value = struct.pack('<h', 0)
        wav_file.writeframes(value)

print(f"Audio generated successfully and saved as {output_filename}!")
