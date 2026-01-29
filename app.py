import streamlit as st
import edge_tts
import asyncio
import base64

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="SpeechForge",
    page_icon="logo.jpg",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS STYLING ---
st.markdown("""
    <style>
        /* A. BACKGROUND (Aurora) */
        [data-testid="stAppViewContainer"] {
            background-color: #020617;
            background-image: 
                radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
                radial-gradient(at 50% 0%, hsla(225,39%,30%,1) 0, transparent 50%), 
                radial-gradient(at 100% 0%, hsla(339,49%,30%,1) 0, transparent 50%);
            background-size: 200% 200%;
            animation: aurora 15s ease infinite;
        }
        @keyframes aurora {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* B. TYPOGRAPHY & CARDS */
        .mega-title {
            font-family: 'Inter', sans-serif;
            font-weight: 900;
            font-size: 64px !important; /* Desktop Size */
            text-align: center;
            background: linear-gradient(to right, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }

        /* --- MOBILE FIX START --- */
        @media only screen and (max-width: 600px) {
            .mega-title {
                font-size: 40px !important; /* Smaller size for mobile */
            }
        }
        /* --- MOBILE FIX END --- */

        .glass-card {
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-radius: 24px;
            padding: 40px;
            box-shadow: 0 20px 50px -10px rgba(0,0,0,0.5);
            max-width: 950px;
            margin: 0 auto;
        }
        .stTextArea textarea {
            background-color: rgba(30, 41, 59, 0.7) !important;
            border: 1px solid #334155 !important;
            color: #f8fafc !important;
            border-radius: 12px;
        }
        
        /* C. BUTTON STYLING */
        button[kind="primary"] {
            background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important;
            color: white !important;
            font-weight: 700 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 24px !important;
            height: 42px !important;
        }
        button[kind="secondary"] {
            background: transparent !important;
            border: 2px solid #3b82f6 !important;
            color: #60a5fa !important;
            font-weight: 700 !important;
            border-radius: 8px !important;
            padding: 10px 24px !important;
            height: 42px !important;
        }

        /* Hide Clutter */
        #MainMenu, footer, header {visibility: hidden;}
        div[data-testid="column"] { display: flex; align-items: center; justify-content: center; }
    </style>
""", unsafe_allow_html=True)

# --- 3. HELPER FUNCTION (For Perfect Logo Centering) ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

# --- 4. BACKEND ---
VOICES = {
    "🇺🇸 Ava (Premium Female)": "en-US-AvaMultilingualNeural",
    "🇺🇸 Andrew (Premium Male)": "en-US-AndrewMultilingualNeural",
    "🇮🇳 Neerja (Expressive Female)": "en-IN-NeerjaExpressiveNeural",
    "🇮🇳 Prabhat (Professional Male)": "en-IN-PrabhatNeural",
    "🇮🇳 Aarav (Hindi Male)": "hi-IN-MadhurNeural",
    "🇮🇳 Swara (Hindi Female)": "hi-IN-SwaraNeural",
    "🇬🇧 Emma (Soft Female)": "en-GB-EmmaMultilingualNeural",
    "🇬🇧 Ryan (Deep Male)": "en-GB-RyanNeural"
}

async def generate_audio(text, voice, rate, pitch):
    output_file = "speechforge_audio.mp3"
    rate_str = f"{rate:+d}%"
    pitch_str = f"{pitch:+d}Hz"
    communicate = edge_tts.Communicate(text, voice, rate=rate_str, pitch=pitch_str)
    await communicate.save(output_file)
    return output_file

# --- 5. LOGO SECTION (Centered) ---
img_b64 = get_base64_image("logo.jpg")
if img_b64:
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin-top: 20px; margin-bottom: 20px;">
            <img src="data:image/jpg;base64,{img_b64}" width="110" style="border-radius: 10px; box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);">
        </div>
        """,
        unsafe_allow_html=True
    )

# --- 6. HERO SECTION ---
st.markdown('<h1 class="mega-title">SpeechForge</h1>', unsafe_allow_html=True)

st.markdown("""
    <p style="text-align: center; color: #e2e8f0; font-size: 26px; font-weight: 600; margin-bottom: 10px; font-family: 'Inter', sans-serif;">
        The ultimate AI voice studio for creators, developers, and businesses.
    </p>
    <p style="text-align: center; color: #94a3b8; font-size: 18px; font-weight: 400; line-height: 1.6; font-family: 'Inter', sans-serif;">
        Transform text into lifelike speech using next-gen neural audio synthesis.<br>
        Powered by Microsoft Edge T5 & Multilingual AI Models.
    </p>
""", unsafe_allow_html=True)


# --- 7. STUDIO CARD ---
st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    selected_voice = st.selectbox("Select Voice Model", list(VOICES.keys()))
    voice_id = VOICES[selected_voice]
with c2:
    speech_rate = st.slider("Speed", -50, 50, 0)
with c3:
    speech_pitch = st.slider("Pitch", -20, 20, 0)

st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
user_text = st.text_area("Script", height=220, label_visibility="collapsed", placeholder="Type your text here...")

st.markdown('<div style="height: 25px;"></div>', unsafe_allow_html=True)
if st.button("✨ GENERATE AUDIO", type="primary", use_container_width=True):
    if not user_text:
        st.warning("Please enter text.")
    else:
        with st.spinner("Synthesizing..."):
            try:
                audio_file = asyncio.run(generate_audio(user_text, voice_id, speech_rate, speech_pitch))
                st.success("Done!")
                ac1, ac2 = st.columns([3, 1])
                with ac1: st.audio(audio_file)
                with ac2:
                    with open(audio_file, "rb") as f:
                        st.download_button("Download", f, "audio.mp3", "audio/mp3", type="secondary", use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# --- 8. FOOTER ---
st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
if 'credits' not in st.session_state: st.session_state.credits = 10000
st.markdown(f"<div style='text-align: center; color: #475569;'>Credits: {st.session_state.credits} | SpeechForge © 2026</div>", unsafe_allow_html=True)
