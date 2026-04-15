import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, field_validator

from app.emotion import detect_emotion
from app.voice   import generate_speech

# ── App setup ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Empathy Engine",
    description="Dynamic emotional TTS — detects emotion and speaks expressively.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup directories
_APP_DIR = os.path.dirname(__file__)
_AUDIO_DIR = os.path.join(_APP_DIR, "static", "audio")
_STATIC_DIR = os.path.join(_APP_DIR, "static")
_TEMPLATES_DIR = os.path.join(_APP_DIR, "templates")

os.makedirs(_AUDIO_DIR, exist_ok=True)
os.makedirs(_STATIC_DIR, exist_ok=True)
os.makedirs(_TEMPLATES_DIR, exist_ok=True)

# Mount static files (CSS, JS, audio)
app.mount("/static", StaticFiles(directory=_STATIC_DIR), name="static")
app.mount("/audio", StaticFiles(directory=_AUDIO_DIR), name="audio")


# ── Request / Response schemas ────────────────────────────────────────────────
class SpeakRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text must not be empty")
        return v.strip()


class SpeakResponse(BaseModel):
    emotion:           str
    detector_intensity: float   # Raw confidence from emotion model
    boosted_intensity: float    # After keyword analysis
    intensity_label:   str      # "Low" | "Medium" | "High"
    audio_url:         str      # Relative URL the client can GET
    rewritten_text:    str      # Emotionally enhanced text that was spoken
    rate:              int
    volume:            float


# ── Helpers ───────────────────────────────────────────────────────────────────
def _intensity_label(score: float) -> str:
    if score >= 0.75:
        return "High"
    if score >= 0.45:
        return "Medium"
    return "Low"


# ── Endpoints ─────────────────────────────────────────────────────────────────
@app.get("/", summary="Serve frontend")
def root():
    """Serve the main frontend HTML page."""
    index_path = os.path.join(_TEMPLATES_DIR, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path, media_type="text/html")
    return {"status": "ok", "service": "Empathy Engine"}


@app.post("/speak", response_model=SpeakResponse, summary="Generate expressive speech")
def speak(body: SpeakRequest):
    """
    Detect emotion in *body.text*, analyze for emotion-specific keywords,
    modulate TTS parameters with expert vocal techniques, render a .wav file,
    and return metadata + a URL to fetch the audio.
    
    Expert enhancements:
    - Keyword-based intensity boosting (voice coaching expertise)
    - Psychological vocal modulation per emotion
    - Voice actor text rewriting techniques
    """
    try:
        # Step 1 — Emotion detection
        emotion, detector_intensity = detect_emotion(body.text)

        # Step 2 — TTS generation with emotional modulation
        # (includes keyword analysis and intensity boosting)
        result = generate_speech(body.text, emotion, detector_intensity)
        boosted_intensity = result.get("boosted_intensity", detector_intensity)

    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {exc}")

    return SpeakResponse(
        emotion            = emotion,
        detector_intensity = detector_intensity,
        boosted_intensity  = boosted_intensity,
        intensity_label    = _intensity_label(boosted_intensity),
        audio_url          = f"/audio/{result['audio_filename']}",
        rewritten_text     = result["rewritten_text"],
        rate               = result["rate"],
        volume             = result["volume"],
    )


@app.get("/audio/{filename}", summary="Stream generated audio")
def get_audio(filename: str):
    """
    Serve a previously generated .wav file by filename.
    FastAPI's StaticFiles mount handles this automatically, but this
    explicit route adds a 404 with a helpful message.
    """
    path = os.path.join(_AUDIO_DIR, filename)
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="Audio file not found.")
    return FileResponse(path, media_type="audio/wav")