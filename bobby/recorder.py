# part of Bobby, a GTK4 application for practicing English pronunciation with advanced phrases. | Copyright (c) 2025 | License: MIT

"""Audio recording utilities using sounddevice."""

import io
import time
from typing import Optional

import numpy as np
import sounddevice as sd
import soundfile as sf


class Recorder:
    def __init__(self, samplerate: int = 16000, silence_threshold: float = 0.01,
                 device: Optional[int] = None):
        self.samplerate = samplerate
        self.channels = 1
        self.silence_threshold = silence_threshold
        self.device = device

    def record(self, max_duration: float, *, activity_cb: Optional[callable] = None, silence_timeout: float = 3.0) -> bytes:
        """Record audio up to ``max_duration`` seconds.

        Recording stops early if ``silence_timeout`` seconds of silence are
        detected. ``activity_cb`` is called with the current volume level
        (0..1) while recording.
        """

        blocksize = int(0.1 * self.samplerate)  # 100ms blocks
        frames = []
        silence_time = 0.0
        start = time.time()
        with sd.InputStream(samplerate=self.samplerate, channels=self.channels,
                           device=self.device) as stream:
            while time.time() - start < max_duration:
                data, _ = stream.read(blocksize)
                frames.append(data.copy())
                vol = float(np.abs(data).mean())
                if activity_cb:
                    activity_cb(min(vol * 10, 1.0))  # scale roughly to 0..1
                if vol < self.silence_threshold:
                    silence_time += blocksize / self.samplerate
                    if silence_time >= silence_timeout:
                        break
                else:
                    silence_time = 0.0

        audio = np.concatenate(frames, axis=0)
        buf = io.BytesIO()
        sf.write(buf, audio, self.samplerate, format="WAV")
        return buf.getvalue()
