"""
This file contains all things related to the podcast generation and audio processing.
"""
import os
from io import BytesIO
from typing import Optional, Union, Dict, List
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
with open("agents/test_convo.json", "r") as f:
    data = json.load(f)
print(data.keys())
dialogues = []


def call_tts_model(dialogue: str, voice: str, file_name: str, response_format: str = "wav") -> None:
    speech_file_path = "speech.wav" 
    model = "playai-tts"
    voice = "Fritz-PlayAI"
    response_format = "wav"

    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=dialogue,
        response_format=response_format
    )

    response.write_to_file(file_name)
    print(f"Audio saved to {file_name}")

idx_k, idx_c =0,0 #katherine and clay's dialogues indices
for speaker in data["order"]:
    if speaker == "Katherine":
        dialogue = data["katherine"][idx_k]["text"]
        file_name = f"audio_katherine_{idx_k}.wav"
        call_tts_model(dialogue=dialogue, voice="Katherine-PlayAI", file_name=file_name)
        idx_k += 1
    elif speaker == "Clay":
        dialogue = data["clay"][idx_c]["text"]
        file_name = f"audio_clay_{idx_c}.wav"
        call_tts_model(dialogue=dialogue, voice="Clay-PlayAI", file_name=file_name)
        idx_c += 1

print(dialogues)