# part of Bobby, a GTK4 application for practicing English pronunciation with advanced phrases. | Copyright (c) 2025 | License: MIT

"""Utilities wrapping OpenAI API for text-to-speech and speech-to-text."""

import io
import os
from typing import Iterable

import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Expect environment variable OPENAI_API_KEY
openai.api_key = os.environ["OPENAI_API_KEY"]
openai_client = openai.OpenAI()

def tts_synthesize(text: str, voice: str = "alloy") -> bytes:
    """Synthesize text to speech using OpenAI's TTS API.

    Returns raw MP3 bytes.
    """
    response = openai_client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
    )
    return response.content


def stt_transcribe(wav_bytes: bytes) -> str:
    """Transcribe audio using OpenAI's STT API."""
    audio_file = io.BytesIO(wav_bytes)
    audio_file.name = "speech.wav"
    response = openai_client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
    )
    return response.text
