## Prompt for Generating a GTK4 Desktop App Specification

---

**Title:**
Build a GTK4 desktop application called **“Bobby”** to help advanced English learners practice and perfect their pronunciation.

**Requirements and Constraints:**

1. **Purpose:**
   The application enables users to improve their English pronunciation by practicing advanced phrases, hearing them spoken aloud, repeating them, and receiving feedback until their pronunciation is accurate.

2. **Features:**

   * Display advanced English phrases (idioms, collocations, complex sentences) to the user.
   * Use the **OpenAI API** for text-to-speech (TTS) to synthesize and play the target phrase in standard English.
   * Allow the user to record their own pronunciation of the phrase via microphone.
   * Use the **OpenAI API** for speech-to-text (STT) transcription of the user’s recorded audio.
   * Compare the transcribed user attempt to the original phrase, highlighting any differences.
   * Provide feedback indicating which words were omitted, mispronounced, or substituted—based strictly on the transcription comparison (since phoneme-level feedback is not natively supported by these APIs).
   * Let the user retry until the spoken phrase matches the original.
   * Track user progress, storing attempts and displaying performance over time.

3. **Technical Scope and Limitations:**

   * **Platform:**

     * Use GTK4 for cross-platform desktop support (Linux, Windows, macOS where feasible).
     * UI should be native to the desktop, not web-based.
   * **Voice Generation:**

     * Integrate OpenAI API for all TTS functionality. Specify available voices/accents and document any parameters that can be adjusted (speed, pitch, etc.).
   * **Transcription:**

     * Use OpenAI API for STT. Specify real-world accuracy with non-native speakers, latency, and input file restrictions.
   * **Feedback Mechanism:**

     * Feedback is limited by what the APIs return—do not promise phoneme-level error detection unless the API supports it.
     * Emphasize word-level comparison: mismatches, omissions, substitutions.
   * **Privacy and Data Handling:**

     * Clearly state how voice data is handled and whether recordings are retained locally or sent to the cloud for processing (per OpenAI API requirements).
   * **Extensibility:**

     * App architecture should make it straightforward to replace or extend speech APIs if future improvements are available.

4. **User Experience:**

   * GTK4-native design: clear phrase presentation, easy recording and playback, real-time feedback.
   * Accessible and responsive interface with modern design cues.
   * Statistics and progress tracking.
   * Optionally display phonetic transcriptions (IPA) if available from API or via open-source libraries.


---

**Instruction:**
“Generate a detailed GTK4 desktop app specification that reflects the above requirements and constraints, focusing on user journey, technical feasibility, and realistic feedback mechanisms, considering the actual capabilities and limitations of Gemini and OpenAI APIs for TTS and STT. Do not generate code. Produce a design document and highlight any technical or UX challenges that would require further research or workaround.”
