import os
import requests
import json
from local_ear import record_and_transcribe
from local_heart import get_emotion

def ask_ollama(prompt, emotion):
    url = "http://localhost:11434/api/generate"
    # We tell the brain how to act based on the emotion detected!
    full_prompt = f"The user feels {emotion}. Act as a cute, empathetic companion. User says: {prompt}"
    
    payload = {
        "model": "llama3",
        "prompt": full_prompt,
        "stream": False
    }
    
    response = requests.post(url, json=payload)
    return response.json()['response']

print("--- LOCAL LUMI IS READY (No API needed) ---")

while True:
    # 1. Sense (Ear)
    user_text = record_and_transcribe(duration=4)
    print(f"🎤 You: {user_text}")
    
    # 2. Feel (Heart)
    emotion_data = get_emotion(user_text)
    emotion_label = emotion_data['label']
    print(f"💙 Lumi senses you feel: {emotion_label}")
    
    # 3. Think (Brain)
    lumi_response = ask_ollama(user_text, emotion_label)
    print(f"🌸 Lumi: {lumi_response}\n")
