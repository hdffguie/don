import os
import requests
import subprocess
import sys

REPO_ID = "rhasspy/piper-voices"
BRANCH = "main"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def list_hf_directory(path):
    """HuggingFace repo ke andar ki files/folders ki list nikalta hai"""
    url = f"https://huggingface.co/api/models/{REPO_ID}/tree/{BRANCH}/{path}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"⚠️ Could not list directory {path}: {e}")
        return []

def find_hindi_voice():
    """Hindi (hi) folder ke andar jaakar automatically pehli available voice dhoondhta hai"""
    print("🔍 Scanning HuggingFace for available Hindi voices...")
    
    level1 = list_hf_directory("hi")  # e.g., hi_IN
    for item1 in level1:
        if item1["type"] == "directory":
            lang_path = item1["path"]  # hi/hi_IN
            level2 = list_hf_directory(lang_path)
            
            for item2 in level2:
                if item2["type"] == "directory":
                    voice_path = item2["path"]  # hi/hi_IN/xxxxx
                    level3 = list_hf_directory(voice_path)
                    
                    for item3 in level3:
                        if item3["type"] == "directory":
                            quality_path = item3["path"]  # hi/hi_IN/xxxxx/medium
                            level4 = list_hf_directory(quality_path)
                            
                            for file in level4:
                                if file["path"].endswith(".onnx"):
                                    onnx_path = file["path"]
                                    json_path = onnx_path + ".json"
                                    print(f"🎯 Found Voice: {onnx_path}")
                                    return onnx_path, json_path
    return None, None

def download_file(path, filename):
    if not os.path.exists(filename):
        url = f"https://huggingface.co/{REPO_ID}/resolve/{BRANCH}/{path}"
        print(f"📥 Downloading {filename} from {url}...")
        r = requests.get(url, headers=HEADERS, timeout=60)
        if r.status_code == 200:
            with open(filename, "wb") as f:
                f.write(r.content)
            print(f"✅ {filename} Downloaded Successfully!")
        else:
            print(f"❌ Failed with status {r.status_code}")
            sys.exit(1)

def generate_voice():
    text = "दोस्तों, क्या आप जानते हैं कि सिर्फ चौबीस घंटे में एक चैनल पर चौदह हज़ार सब्सक्राइबर आ सकते हैं? मैं रात तीन बजे तक एडिटिंग करता रहा, फिर भी मेरी वीडियो पर एक भी व्यूज़ नहीं आया। सच कहूँ तो, स्मार्ट लोग अब खुद एडिटिंग नहीं करते, वो एक्सपर्ट टीम को आउटसोर्स करते हैं। हमारी टीम आपके लिए स्क्रिप्ट लिखेगी, वीडियो एडिट करेगी, और सीधे आपके चैनल पर अपलोड कर देगी। बेसिक प्लान सिर्फ चार सौ निन्यानवे रुपये में, रोज़ाना एक वीडियो की गारंटी के साथ। आज ही मौका पकड़ लो, अभी डीएम करो ग्रो, और अपने चैनल को आसमान तक पहुँचाओ!"
    output_file = "piper_test_voice.wav"
    
    print(f"⏳ Generating High-Quality Voice for: '{text}'...")
    safe_text = text.replace('"', '\\"').replace("'", "\\'")
    cmd = f'echo "{safe_text}" | piper --model model.onnx --output_file {output_file}'
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ BOOM! Piper Voice successfully generated: {output_file}")
    except Exception as e:
        print(f"❌ Voice Generation Failed: {e}")

if __name__ == "__main__":
    onnx_path, json_path = find_hindi_voice()
    
    if onnx_path:
        download_file(onnx_path, "model.onnx")
        download_file(json_path, "model.onnx.json")
        generate_voice()
    else:
        print("❌ No Hindi voice found in the repository!")
