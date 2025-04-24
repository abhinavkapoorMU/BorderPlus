# BorderPlus

Starting with Workflow

This is a browser-based prototype to help nurses practice and improve their spoken German.  
Users can listen to a phrase, speak it back, and get instant feedback on their pronunciation accuracy.  
It’s fast, free, and works entirely in the browser.

-----

## ✅ Prerequisites

1. Python 3.1+ installed with pip.
2. FFmpeg installed (required by Whisper for audio processing):
   - *macOS:* brew install ffmpeg
   - *Ubuntu/Debian:* sudo apt install ffmpeg
-----

## ⚙️ Workflow Engine Local Setup 

1. Clone the repo:
   git clone https://github.com/your-username/german-pronunciation-coach.git
   cd german-pronunciation-coach
  
2. Install dependencies:
   pip install -r requirements.txt

3. Run the Streamlit app:
   streamlit run app.py

4. Open your browser and go to:
   http://localhost:8501

-----

## 🧠 Tech Stack

- [Streamlit](https://streamlit.io/)
- [Whisper (open-source)](https://github.com/openai/whisper)
- [gTTS](https://pypi.org/project/gTTS/)
- [streamlit-mic-recorder](https://pypi.org/project/streamlit-mic-recorder/)
- Python built-ins: difflib, tempfile, os

-----

## Steps

1. Launch the app.
2. Choose a German phrase from the dropdown (5 preset phrases).
3. Listen to the phrase using gTTS playback.
4. Record your own pronunciation using the built-in mic.
5. App transcribes your audio using the local Whisper model.
6. Displays:
   - Your transcription
   - Similarity score (0–100%)
   - Color-coded feedback (🟢 good, 🟡 okay, 🔴 needs improvement)
7. Retry to improve — progress is tracked with a score history chart.

-----

## Challenges Faced

- Handling binary audio data from browser mic correctly
- Whisper model can take time to transcribe — local performance tuning helps
- Ensuring feedback is helpful without being discouraging

-----

## 🚀 What You’d Need To Go Live

- A hosted backend or GPU-enabled VM (for faster Whisper transcription)
- User login system for personalized phrase tracking
- A/b testing variants of UI feedback mechanisms
- Mobile optimizations and internationalization
- Optional: Replace gTTS with offline TTS like Coqui-TTS for full offline support
