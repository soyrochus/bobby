# Improving Functionality and Visual Feedback in “Bobby” Pronunciation App

---

**Context:**
The current GTK4-based application for “Bobby” has a working UI. The layout, navigation, and phrase lists are functional. However, key aspects of the interactive pronunciation workflow are not yet implemented or lack clear user feedback.

**Required Improvements:**

1. **Practice Button Functionality**

   * When the user presses the practice button (microphone/play icon) next to a phrase:

     * The app should use the AI service (OpenAI or Gemini API) to synthesize the spoken version of the phrase (Text-to-Speech).
     * The generated audio should be played back to the user through the system’s speakers.
     * While audio is playing, a clear visual indication (e.g., animation, color change, progress bar, or icon change) should show that playback is in progress.

2. **Recording User Speech**

   * After playback, the app should prompt the user (visually and, optionally, audibly) to repeat the phrase.
   * A prominent visual indicator should signal that the app is now **recording** (e.g., animated microphone, pulsing border, or color transition).
   * The app records the student’s spoken attempt.

3. **Analysis and Feedback**

   * The recorded audio should be sent to the AI service (OpenAI or Gemini API) for speech-to-text transcription and pronunciation analysis.
   * The analysis results should be displayed on the UI:

     * Clearly highlight which parts of the phrase were pronounced correctly or incorrectly.
     * Provide actionable, readable feedback (e.g., missed words, mispronunciations).
     * Optionally, display suggestions or encouragement.

4. **Visual Feedback is Essential**

   * At every stage, the user must have **clear, intuitive visual cues** about what the app is doing:

     * **Playback in progress**
     * **Recording in progress**
     * **Analysis/result display**
   * Feedback should be accessible and unambiguous, using color, iconography, animation, or progress indicators as appropriate.

---

**Instruction:**
“Update the current application so that pressing the practice button triggers the full pronunciation workflow: (1) plays the AI-generated phrase audio, (2) prompts and records the user’s speech with clear visual indication, (3) analyzes the recording with the AI, and (4) displays results with actionable feedback. At each step, provide strong, user-friendly visual cues reflecting the current state (playing, recording, analyzing, result). Do not change the overall UI layout—focus on implementing these functional and feedback elements to make the practice experience intuitive and interactive.”

