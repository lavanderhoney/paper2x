"""
This file contains all things related to the podcast generation and audio processing.
"""
import os
import json
import requests
from io import BytesIO
from datetime import datetime
from typing import Optional, Union, Dict, List
from groq import Groq
from dotenv import load_dotenv
from murf import Murf
from pydub import AudioSegment
load_dotenv()
client = Murf(api_key=os.getenv("MURF_API_KEY"))
# dialogues = []

def call_tts_model(dialogue: str, voice: str, file_name: str) -> None:
    try:
        res = client.text_to_speech.generate(
            text=dialogue,
            voice_id=voice,
        )
        audio_url = res.audio_file
        response = requests.get(audio_url)
        if response.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(response.content)
        else:
            print(f"Failed to download audio: {response.status_code}")
        print(f"Audio saved to {file_name}")
    except Exception as e:
        print(f"Error generating audio for '{dialogue[:30]}...': {e}")
    return

def generate_clips(data: dict, KATHERINE_VOICE: str, CLAY_VOICE: str) -> List[str]:
    """
    Generate audio clips for the given dialogues using specified voices.
    Args:
        data (dict): Dictionary containing dialogue data from LLM.
        KATHERINE_VOICE (str): Voice ID for Katherine.
        CLAY_VOICE (str): Voice ID for Clay.
    Returns:
        List[str]: List of file paths to the generated audio clips.
    """
    idx_k, idx_c =0,0 #katherine and clay's dialogues indices
    clips_sequences = []
    for speaker in data["order"]:
        try:
            if speaker == "Katherine":
                dialogue = data["katherine"][idx_k]["text"]
                file_name = f"audio/audio_katherine_{idx_k}.wav"
                call_tts_model(dialogue=dialogue, voice=KATHERINE_VOICE, file_name=file_name)
                idx_k += 1
            elif speaker == "Clay":
                dialogue = data["clay"][idx_c]["text"]
                file_name = f"audio/audio_clay_{idx_c}.wav"
                call_tts_model(dialogue=dialogue, voice=CLAY_VOICE, file_name=file_name)
                idx_c += 1
            clips_sequences.append(file_name)
        except Exception as e:
            print(f"Error creating audio for speaker '{speaker}': {e}")
            break
    return clips_sequences
   
def combine_audio_files(audio_files, output_file:str = "podcast.wav"):
    final_clip = AudioSegment.empty()
    for clip_path in audio_files:
        audio = AudioSegment.from_wav(clip_path)
        final_clip += audio
        final_clip += AudioSegment.silent(duration=1000)
    final_clip.export(output_file, format="wav")
    print(f"Combined audio saved to {output_file}")

def generate_podcast(data: dict, KATHERINE_VOICE: str = "en-US-ariana", CLAY_VOICE: str = "en-US-miles") -> str:
    """
    Main pipeline function to generate the podcast, which is called in agent.py by the graph workflow.
    Args:
        data (dict): output from the LLM's output parser. Follows the structure defined in the Conversation model.
        KATHERINE_VOICE (str): Voice ID for Katherine.
        CLAY_VOICE (str): Voice ID for Clay.
    Returns:
        str: Path to the generated podcast audio file.
    """
    clips_sequences = generate_clips(data, KATHERINE_VOICE, CLAY_VOICE)
    print(f"Audio clips sequence: {clips_sequences}")

    timestamp = datetime.timestamp(datetime.now())
    podcast_file = f"podcast_{timestamp}.wav"

    combine_audio_files(clips_sequences, podcast_file)
    
    return podcast_file



if __name__ == "__main__":
    with open("agents/test_convo.json", "r") as f:
        data = json.load(f)
    print(data.keys())
    KATHERINE_VOICE = "en-US-ariana"
    CLAY_VOICE = "en-US-miles"
    generate_podcast(data, KATHERINE_VOICE, CLAY_VOICE)
