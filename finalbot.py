import urllib
import streamlit as st
import difflib
import tempfile
import os
from gtts import gTTS
import whisper
from streamlit_mic_recorder import mic_recorder
import ssl
import numpy as np
from sklearn.linear_model import LinearRegression

# Bypass SSL verification if needed (for Whisper downloads)
ssl._create_default_https_context = ssl._create_unverified_context

# Load Whisper model locally
model = whisper.load_model("base")

# Preset German phrases
PHRASES = {
    "How are you?": "Wie geht es Ihnen?",
    "Thank you very much": "Vielen Dank",
    "Where is the hospital?": "Wo ist das Krankenhaus?",
    "I need help": "Ich brauche Hilfe",
    "Do you feel pain?": "Haben Sie Schmerzen?"
}

st.title("🗣️ German Pronunciation Coach for Nurses")
st.markdown("Select a phrase, listen to it, repeat it, and get instant feedback!")

# Phrase selection
selected_key = st.selectbox("Choose a phrase:", list(PHRASES.keys()))
selected_phrase = PHRASES[selected_key]

st.write(f"### German Phrase: {selected_phrase}")

# Play the phrase using gTTS
tts = gTTS(text=selected_phrase, lang='de')
audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
tts.save(audio_file.name)

with open(audio_file.name, "rb") as f:
    audio_bytes = f.read()
st.audio(audio_bytes, format='audio/mp3')

# Record user audio using mic
st.markdown("### Record your pronunciation")
audio_dict = mic_recorder(start_prompt="Start recording", stop_prompt="Stop recording", use_container_width=True)

if audio_dict and "bytes" in audio_dict:
    user_audio_bytes = audio_dict["bytes"]
    st.audio(user_audio_bytes)

    with st.spinner("Processing audio..."):
        try:
            uploaded_audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
            with open(uploaded_audio_path, "wb") as f:
                f.write(user_audio_bytes)

            result = model.transcribe(uploaded_audio_path)
            transcript = result["text"].strip()
            st.success("Transcription complete")
        except Exception as e:
            st.error(f"Error during transcription: {str(e)}")
            transcript = ""

    if transcript:
        st.markdown(f"*You said:* {transcript}")
        sm = difflib.SequenceMatcher(None, selected_phrase.lower(), transcript.lower())
        score = round(sm.ratio() * 100, 2)

        st.markdown(f"### 🎯 Similarity Score: *{score}%*")
        if score > 72:
            st.success("Great job! 🟢")
        elif score > 50:
            st.warning("Good try! 🟡")
        else:
            st.error("Keep practicing! 🔴")

        # Store scores and show chart
        if "scores" not in st.session_state:
            st.session_state.scores = []

        st.session_state.scores.append(score)
        scores_array = np.array(st.session_state.scores)

        st.line_chart(scores_array, height=150)

        # Calculate slope using linear regression
        if len(scores_array) > 1:
            X = np.arange(len(scores_array)).reshape(-1, 1)
            y = scores_array.reshape(-1, 1)
            model_lr = LinearRegression().fit(X, y)
            slope = round(model_lr.coef_[0][0], 2)

            if slope > 0:
                st.success(f"📈 You're improving! Trend slope: +{slope}")
            elif slope < 0:
                st.warning(f"📉 Slight decline in performance. Trend slope: {slope}")
            else:
                st.info("➖ No noticeable change in trend yet. Keep practicing!")

# Cleanup
audio_file.close()
os.unlink(audio_file.name)
