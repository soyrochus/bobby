# part of Bobby, a GTK4 application for practicing English pronunciation with advanced phrases. | Copyright (c) 2025 | License: MIT

"""Audio recording utilities using sounddevice."""

import io
from typing import Optional

import numpy as np
import sounddevice as sd
import soundfile as sf


class Recorder:
    def __init__(self, samplerate: int = 16000):
        self.samplerate = samplerate
        self.channels = 1

    def record(self, duration: float) -> bytes:
        """Record audio for a fixed duration and return WAV bytes."""
        audio = sd.rec(int(duration * self.samplerate), samplerate=self.samplerate, channels=self.channels, dtype=np.float32)
        sd.wait()
        buf = io.BytesIO()
        sf.write(buf, audio, self.samplerate, format="WAV")
        return buf.getvalue()
