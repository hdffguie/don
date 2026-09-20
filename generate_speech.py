import os
from huggingface_hub import snapshot_download

# 1. मॉडल डाउनलोड करें (यदि पहले से लोकली सेव नहीं है)
# आप यहाँ कम्युनिटी का हिंदी मॉडल 'tarun7r/vibevoice-hindi-1.5B' भी दे सकते हैं
model_repo = "vibevoice-community/VibeVoice-1.5B" 
print("Downloading VibeVoice Model...")
model_path = snapshot_download(repo_id=model_repo)

# 2. VibeVoice के इनफ्रेंस लाइब्रेरी को इम्पोर्ट करें
# (सुनिश्चित करें कि रिपो का स्ट्रक्चर सही पाथ पर हो)
from vibevoice.inference import VibeVoiceTTS 

def text_to_speech_hindi():
    text_input = "नमस्कार, यह GitHub Actions और VibeVoice AI द्वारा जनरेट की गई हिंदी आवाज़ है।"
    output_audio = "hindi_output.wav"
    
    print(f"Synthesizing text: '{text_input}'")
    
    # मॉडल लोड करें
    tts = VibeVoiceTTS(model_path=model_path)
    
    # स्पीच जनरेट करें (आप अपनी पसंद के स्पीकर का नाम दे सकते हैं)
    tts.generate(
        text=text_input,
        output_path=output_audio,
        speaker_name="Default_Hindi_Voice"
    )
    
    print(f"Audio successfully saved to {output_audio}")

if __name__ == "__main__":
    text_to_speech_hindi()
