"""
This file contains all things related to the podcast generation and audio processing.
"""
import os
import json
import requests
from io import BytesIO
from datetime import datetime
from typing import Optional, Union, Dict, List
from dotenv import load_dotenv
from murf import Murf
from pydub import AudioSegment
load_dotenv()
client = Murf(api_key=os.getenv("MURF_API_KEY"))
# dialogues = []

def call_tts_model(dialogue: str, voice: str) -> AudioSegment:
    try:
        res = client.text_to_speech.generate(
            text=dialogue,
            voice_id=voice,
            format="mp3",
        )
        audio_url = res.audio_file
        response = requests.get(audio_url)
        response.raise_for_status()  
        
        #rather than saving individual clips, keep them in memory as AudioSegment objects
        audio = AudioSegment.from_file(BytesIO(response.content), format="mp3")
        return audio
    except Exception as e:
        print(f"Error generating audio for '{dialogue[:30]}...': {e}")
        raise e
def generate_clips(data: dict, KATHERINE_VOICE: str, CLAY_VOICE: str) -> List[AudioSegment]:
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
    
    # Ensure the order is present in the data
    if "order" not in data:
        raise ValueError("Data must contain 'order' key to determine dialogue sequence.")
    for speaker in data["order"]:
        try:
            if speaker.lower() == "katherine":
                dialogue = data["katherine"][idx_k]["text"]
                clips_sequences.append(call_tts_model(dialogue=dialogue, voice=KATHERINE_VOICE))
                idx_k += 1
                print(f"Generated audio for Katherine: {dialogue[:30]}...")  # Debugging output
            elif speaker.lower() == "clay":
                dialogue = data["clay"][idx_c]["text"]
                clips_sequences.append(call_tts_model(dialogue=dialogue, voice=CLAY_VOICE))
                idx_c += 1
                print(f"Generated audio for Clay: {dialogue[:30]}...")  # Debugging output
        except Exception as e:
            print(f"Error creating audio for speaker '{speaker}': {e}")
            raise e
    return clips_sequences

# also changing this to use AudioSegment instead of individual clips' file paths
def combine_audio_files(audio_files: List[AudioSegment], output_file:str = "podcast.mp3") -> None:
    final_clip = AudioSegment.empty()
    try:
        for audio in audio_files:
            final_clip += audio
            final_clip += AudioSegment.silent(duration=1000)
        final_clip.export(output_file, format="mp3") # Save as MP3, WAV too large
        print(f"Combined audio saved to {output_file}")
    except Exception as e:
        print(f"Error combining audio files: {e}")
        raise e

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
    if not clips_sequences:
        raise ValueError("No audio clips generated.")
    print(f"Audio clips sequence: {clips_sequences}")

    timestamp = datetime.timestamp(datetime.now())
    podcast_file = f"podcast_{timestamp}.mp3"

    combine_audio_files(clips_sequences, podcast_file)
    print("podcast_file:", podcast_file)
    return podcast_file



if __name__ == "__main__":
    with open("backend\\test_convo.json", "r") as f:
        data = json.load(f)
    print(data.keys())
    KATHERINE_VOICE = "en-US-ariana"
    CLAY_VOICE = "en-US-miles"
    generate_podcast(data, KATHERINE_VOICE, CLAY_VOICE)
