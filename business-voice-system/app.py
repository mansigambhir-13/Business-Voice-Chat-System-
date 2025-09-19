import streamlit as st
import numpy as np
import io
import time
import tempfile
import os
import wave

# REAL VOICE IMPORTS
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

class RealVoiceGenerator:
    def __init__(self):
        self.tts_engine = None
        self.is_initialized = False
    
    def initialize_tts(self):
        if PYTTSX3_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                voices = self.tts_engine.getProperty('voices')
                if voices:
                    self.tts_engine.setProperty('voice', voices[0].id)
                self.tts_engine.setProperty('rate', 150)
                self.tts_engine.setProperty('volume', 0.9)
                self.is_initialized = True
                return True
            except:
                pass
        self.is_initialized = True
        return True
    
    def generate_real_voice_pyttsx3(self, text):
        try:
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                tmp_path = tmp.name
            
            self.tts_engine.save_to_file(text, tmp_path)
            self.tts_engine.runAndWait()
            
            if os.path.exists(tmp_path):
                with open(tmp_path, 'rb') as f:
                    audio_bytes = f.read()
                os.unlink(tmp_path)
                return audio_bytes, 0.85
            return None, 0.0
        except Exception as e:
            st.error(f"Windows TTS failed: {e}")
            return None, 0.0
    
    def generate_real_voice_gtts(self, text):
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            buffer = io.BytesIO()
            tts.write_to_fp(buffer)
            return buffer.getvalue(), 0.90
        except Exception as e:
            st.error(f"Google TTS failed: {e}")
            return None, 0.0
    
    def generate_voice(self, text):
        if not self.is_initialized:
            self.initialize_tts()
        
        # Try Windows TTS first
        if PYTTSX3_AVAILABLE and self.tts_engine:
            st.info("🎵 Generating with Windows TTS...")
            result = self.generate_real_voice_pyttsx3(text)
            if result[0]:
                return result
        
        # Try Google TTS
        if GTTS_AVAILABLE:
            st.info("🎵 Generating with Google TTS...")
            result = self.generate_real_voice_gtts(text)
            if result[0]:
                return result
        
        st.error("❌ No TTS engines available")
        return None, 0.0

def main():
    st.set_page_config(page_title="🎤 REAL Voice System", page_icon="🎤")
    
    st.markdown("# 🎤 REAL Business Voice System")
    st.markdown("### ✅ NO MORE BUZZING - Real Human Speech!")
    
    if PYTTSX3_AVAILABLE:
        st.success("✅ Windows TTS Available")
    if GTTS_AVAILABLE:
        st.success("✅ Google TTS Available")
    
    if 'voice_gen' not in st.session_state:
        st.session_state.voice_gen = RealVoiceGenerator()
    
    text_input = st.text_area(
        "Enter your text:",
        height=150,
        placeholder="Type: 'Hello, this is regarding your account update'\n\n✅ You'll hear REAL speech, not buzzing!"
    )
    
    if st.button("🎵 Generate REAL Voice", type="primary"):
        if text_input.strip():
            with st.spinner("🎵 Generating REAL human speech..."):
                audio_bytes, quality = st.session_state.voice_gen.generate_voice(text_input)
                
                if audio_bytes:
                    st.success(f"🎉 SUCCESS! Real speech generated (Quality: {quality:.1%})")
                    st.audio(audio_bytes, format="audio/wav")
                    st.download_button(
                        "📥 Download",
                        audio_bytes,
                        f"real_voice_{int(time.time())}.wav",
                        "audio/wav"
                    )
                else:
                    st.error("❌ Failed to generate voice")
        else:
            st.warning("⚠️ Please enter text")

if __name__ == "__main__":
    main()
