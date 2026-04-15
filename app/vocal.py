import os
import time
import pyttsx3

from app.config import (
    calculate_keyword_intensity_boost,
    get_voice_params,
    rewrite_text,
)

# ── Output directory ──────────────────────────────────────────────────────────
_AUDIO_DIR = os.path.join(os.path.dirname(__file__), "static", "audio")
os.makedirs(_AUDIO_DIR, exist_ok=True)


def generate_speech(text: str, emotion: str, intensity: float) -> dict:

   
    if not text or not text.strip():
        raise ValueError("Text input is empty.")

    # ── 1. Boost intensity based on emotion-specific keywords ──────────────────
    keyword_boost = calculate_keyword_intensity_boost(text, emotion)
    boosted_intensity = min(1.0, intensity + keyword_boost)

    # ── 2. Get optimal voice parameters for this emotion + boosted intensity ───
    voice_params = get_voice_params(emotion, boosted_intensity)
    final_rate = voice_params["rate"]
    final_volume = voice_params["volume"]
    voice_index = voice_params["voice_index"]

    # ── 3. Rewrite text for natural, authentic delivery ───────────────────────
    spoken_text = rewrite_text(text, emotion, boosted_intensity)

    # ── 4. Initialize pyttsx3 engine ──────────────────────────────────────────
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")

    # Select voice by index; fall back to index 0 if not enough voices
    if voices and voice_index < len(voices):
        engine.setProperty("voice", voices[voice_index].id)
    elif voices:
        engine.setProperty("voice", voices[0].id)

    engine.setProperty("rate", final_rate)
    engine.setProperty("volume", final_volume)

    # ── 5. Save audio file ────────────────────────────────────────────────────
    filename = f"{emotion}_{int(time.time())}.wav"
    audio_path = os.path.join(_AUDIO_DIR, filename)

    engine.save_to_file(spoken_text, audio_path)
    engine.runAndWait()

    return {
        "audio_filename": filename,
        "audio_path": audio_path,
        "rewritten_text": spoken_text,
        "rate": final_rate,
        "volume": final_volume,
        "detector_intensity": intensity,
        "boosted_intensity": boosted_intensity,
    }
