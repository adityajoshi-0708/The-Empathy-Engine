from transformers import pipeline

# ── Load once at import time ──────────────────────────────────────────────────
# top_k=None → returns scores for ALL emotion classes (we pick the winner)
_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None,
)

# ── Label normalisation ───────────────────────────────────────────────────────
# The model returns labels like "joy", "anger", etc.
# We keep them as-is; voice.py maps them to TTS parameters.
# "disgust" is mapped → "anger" since they share similar vocal delivery.
_LABEL_REMAP = {
    "disgust": "anger",
}


def detect_emotion(text: str) -> tuple[str, float]:
    """
    Analyse *text* and return (emotion, intensity).

    Parameters
    ----------
    text : str
        Raw input text from the user.

    Returns
    -------
    emotion : str
        One of: joy | anger | sadness | fear | surprise | neutral
    intensity : float
        Confidence score in [0.0, 1.0].  Higher → stronger modulation.
    """
    text = text.strip()
    if not text:
        return "neutral", 0.5

    # Run inference; result is a list of [{label, score}, ...]
    raw: list[dict] = _classifier(text)[0]

    # Build a clean dict for easy lookup
    scores: dict[str, float] = {item["label"]: item["score"] for item in raw}

    # Pick the highest-scoring emotion
    emotion: str = max(scores, key=scores.get)
    intensity: float = round(scores[emotion], 4)

    # Normalise edge-case labels
    emotion = _LABEL_REMAP.get(emotion, emotion)

    return emotion, intensity