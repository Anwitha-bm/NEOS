import streamlit as st
import pyttsx3
import requests
import os
import base64

#CONFIGURATION
HF_API_TOKEN = "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"  # <-- Replace with your token
TTS_MODEL_ID = "ibm/tts_granite_large"
PARAPHRASE_MODEL_ID = "tuner007/pegasus_paraphrase"
GRANITE_TTS_API_URL = f"https://api-inference.huggingface.co/models/{TTS_MODEL_ID}"
PARAPHRASE_API_URL = f"https://api-inference.huggingface.co/models/{PARAPHRASE_MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

#PAGE SETUP
st.set_page_config(page_title="NeoSonic - AI Audiobook Creator", layout="wide")
st.title("NeoSonic - AI Audiobook Creator")
st.write("🎧 Convert text into expressive audiobooks using IBM Granite (Online) or Granite (Offline) with optional paraphrasing.")

#BACKGROUND CUSTOMIZATION
with st.sidebar:
    st.header("🎨 Background Settings")

    # Color picker
    bg_color = st.color_picker("Pick a background color", "#9898d8")

    # Wallpaper uploader
    uploaded_wallpaper = st.file_uploader("Upload custom wallpaper", type=["png", "jpg", "jpeg"])

    # Apply background
    if uploaded_wallpaper:
        img_bytes = uploaded_wallpaper.read()
        encoded = base64.b64encode(img_bytes).decode()
        css = f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """
    else:
        css = f"""
        <style>
        .stApp {{
            background: {bg_color};
        }}
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

#SESSION STATE FOR HISTORY
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar stickers & History
with st.sidebar:
    st.header("Customize Your UI")
    stickers = {
        "🎧 Headphones": "https://cdn-icons-png.flaticon.com/512/727/727245.png",
        "📚 Book": "https://cdn-icons-png.flaticon.com/512/29/29302.png",
        "🎤 Microphone": "https://cdn-icons-png.flaticon.com/512/727/727240.png",
        "🎵 Music Note": "https://cdn-icons-png.flaticon.com/512/727/727269.png"
    }
    chosen_sticker = st.selectbox("Choose a sticker for the app", list(stickers.keys()))
    st.image(stickers[chosen_sticker], width=100)

    st.markdown("---")
    st.header("🕘 History")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history), 1):
            with st.expander(f"Entry {i} - Tone: {item['tone']} | Engine: {item['engine']}"):
                st.markdown("**Original Text:**")
                st.write(item["original_text"])
                if item.get("rewritten_text") and item["rewritten_text"] != item["original_text"]:
                    st.markdown("**Rewritten Text:**")
                    st.write(item["rewritten_text"])
    else:
        st.write("No history yet.")

#TEXT INPUT
uploaded_file = st.file_uploader("📂 Upload a text file", type=["txt"])
text_input = st.text_area("✍️ Or paste your text here", height=200)

text_data = ""
if uploaded_file:
    text_data = uploaded_file.read().decode("utf-8")[:2000]
elif text_input:
    text_data = text_input

#SETTINGS
engine_choice = st.selectbox("🧠 Select TTS Engine", ["IBM Granite (Online)", "Granite (Offline)"])
tone = st.selectbox("🎭 Select Tone", ["Neutral", "Inspiring", "Suspenseful"])
voice = st.selectbox("🎤 Select Voice (Offline only)", ["Default", "Male", "Female"])

#PARAPHRASE FUNCTION
def rewrite_text(text, tone="Neutral"):
    prompt = f"Rewrite this in a {tone.lower()} tone: {text}"
    payload = {"inputs": prompt,"parameters":{"do_sample": True,"top_k": 50,"top_p": 0.95,"num_return_sequences": 1}}
    response = requests.post(PARAPHRASE_API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        results = response.json()
        if isinstance(results, list) and "generated_text" in results[0]:
            return results[0]["generated_text"]
        else:
            return text
    else:
        st.error(f"Paraphrasing Error: {response.status_code}")
        st.text(response.text)
        return text

#IBM GRANITE AUDIO FUNCTION
def generate_granite_audio(text):
    payload = {"inputs": text}
    response = requests.post(GRANITE_TTS_API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        content_type = response.headers.get("Content-Type", "")
        if "audio" in content_type:
            return response.content
        else:
            st.error(f"Unexpected response content type: {content_type}")
            st.text(response.text)
            return None
    else:
        st.error(f"IBM Granite TTS API returned error {response.status_code}")
        st.text(response.text)
        return None

# PYTTSX3 HELPERS
def get_voice_id(engine, voice_name):
    voices = engine.getProperty('voices')
    if voice_name == "Male":
        for v in voices:
            if "male" in v.name.lower():
                return v.id
        return voices[0].id
    elif voice_name == "Female":
        for v in voices:
            if "female" in v.name.lower():
                return v.id
        if len(voices) > 1: return voices[1].id
        return voices[0].id
    else:
        return voices[0].id

def apply_tone(engine, tone_choice):
    if tone_choice == "Neutral":
        engine.setProperty('rate', 150)
    elif tone_choice == "Inspiring":
        engine.setProperty('rate', 170)
    elif tone_choice == "Suspenseful":
        engine.setProperty('rate', 120)

#REWRITE BUTTON
if st.button("🔁 Rewrite Text"):
    if not text_data.strip():
        st.warning("Please provide text first.")
    else:
        with st.spinner("Rewriting using Pegasus model..."):
            rewritten = rewrite_text(text_data, tone)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original Text")
            st.write(text_data)
        with col2:
            st.subheader("Rewritten Text")
            st.write(rewritten)
        st.session_state.history.append({"original_text": text_data,"rewritten_text": rewritten,"tone": tone,"engine": engine_choice})
        text_data = rewritten

#AUDIO GENERATION
if st.button("🎙️ Generate Audio"):
    if not text_data.strip():
        st.warning("Please provide some text first.")
    else:
        audio_bytes = None
        with st.spinner("Generating audio..."):
            if engine_choice == "IBM Granite (Online)":
                audio_bytes = generate_granite_audio(text_data)
            elif engine_choice == "Granite (Offline)":
                engine = pyttsx3.init()
                engine.setProperty("voice", get_voice_id(engine, voice))
                apply_tone(engine, tone)
                temp_audio_path = "output.wav"
                engine.save_to_file(text_data, temp_audio_path)
                engine.runAndWait()
                with open(temp_audio_path, "rb") as f:
                    audio_bytes = f.read()
                os.remove(temp_audio_path)

        if audio_bytes:
            st.session_state.history.append({"original_text": text_data,"rewritten_text": text_data,"tone": tone,"engine": engine_choice})
            st.subheader("🔊 Audio Output")
            st.audio(audio_bytes, format="audio/wav")
            st.download_button("⬇️ Download Audio", data=audio_bytes, file_name="neosonic_output.wav", mime="audio/wav")
        else:
            st.error("Audio generation failed.")

