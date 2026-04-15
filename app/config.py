import re
import random

# ─────────────────────────────────────────────────────────────
# 🔹 EMOTION KEYWORDS (Cleaned + Non-overlapping)
# ─────────────────────────────────────────────────────────────

EMOTION_KEYWORDS = {
    "joy": {
        "high_intensity": [
            "amazing", "awesome", "fantastic", "incredible", "love",
            "thrilled", "excited", "ecstatic", "wow", "yay"
        ],
        "moderate_intensity": [
            "good", "nice", "great", "happy", "glad", "cheerful"
        ]
    },
    "sadness": {
        "high_intensity": [
            "devastated", "heartbroken", "hopeless", "miserable",
            "depressed", "alone", "empty"
        ],
        "moderate_intensity": [
            "sad", "down", "unhappy", "disappointed", "tired"
        ]
    },
    "anger": {
        "high_intensity": [
            "furious", "livid", "hate", "unacceptable",
            "ridiculous", "enough", "fed up"
        ],
        "moderate_intensity": [
            "angry", "annoyed", "frustrated", "irritated"
        ]
    },
    "fear": {
        "high_intensity": [
            "terrified", "panic", "scared", "danger", "help"
        ],
        "moderate_intensity": [
            "afraid", "worried", "nervous", "anxious"
        ]
    },
    "surprise": {
        "high_intensity": [
            "shocking", "unbelievable", "no way"
        ],
        "moderate_intensity": [
            "surprised", "amazed", "unexpected"
        ]
    }
}

# ─────────────────────────────────────────────────────────────
# 🔹 KEYWORD INTENSITY BOOST (FIXED)
# ─────────────────────────────────────────────────────────────

def calculate_keyword_intensity_boost(text: str, emotion: str) -> float:
    """
    Analyzes text for emotion-specific keywords and returns an intensity boost (0.0-0.35).
    Uses word boundaries to avoid partial matches and normalizes by text length.
    """
    if emotion not in EMOTION_KEYWORDS:
        return 0.0

    text_lower = text.lower()
    keywords = EMOTION_KEYWORDS[emotion]

    def count_matches(word_list):
        return sum(
            1 for word in word_list
            if re.search(rf"\b{re.escape(word)}\b", text_lower)
        )

    high_matches = count_matches(keywords.get("high_intensity", []))
    moderate_matches = count_matches(keywords.get("moderate_intensity", []))

    boost = (high_matches * 0.15) + (moderate_matches * 0.08)

    # Normalize by sentence length to prevent overboosting short texts
    length_factor = len(text.split()) / 10 + 1
    boost = boost / length_factor

    return min(boost, 0.35)

# ─────────────────────────────────────────────────────────────
# 🔹 VOICE CONFIG (FIXED + BALANCED)
# ─────────────────────────────────────────────────────────────

VOICE_CONFIG = {
    "joy": {
        "rate": 160,
        "volume": 0.95,
        "voice_index": 1,
        "rate_scale": 24,
        "volume_scale": 0.05,
        "description": "Bright, energetic, with natural peaks of excitement"
    },
    "anger": {
        "rate": 160,
        "volume": 0.9,
        "voice_index": 0,
        "rate_scale": 20,
        "volume_scale": 0.1,
        "description": "Clipped, forceful, controlled restraint with power"
    },
    "sadness": {
        "rate": 125,
        "volume": 0.55,
        "voice_index": 1,
        "rate_scale": -15,
        "volume_scale": -0.08,
        "description": "Deep, slow, vulnerable, with emotional weight"
    },
    "fear": {
        "rate": 140,
        "volume": 0.7,
        "voice_index": 1,
        "rate_scale": -10,
        "volume_scale": -0.05,
        "description": "Hesitant, quick, with vocal tension and uncertainty"
    },
    "surprise": {
        "rate": 160,
        "volume": 1.1,
        "voice_index": 2,
        "rate_scale": 25,
        "volume_scale": 0.15,
        "description": "Rapid, expressive, with vocal catch and breathlessness"
    },
    "neutral": {
        "rate": 150,
        "volume": 0.85,
        "voice_index": 0,
        "rate_scale": 10,
        "volume_scale": 0.0,
        "description": "Steady, professional, informative tone"
    }
}

# ─────────────────────────────────────────────────────────────
# 🔹 APPLY VOICE WITH INTENSITY
# ─────────────────────────────────────────────────────────────

def get_voice_params(emotion: str, intensity: float) -> dict:
    """
    Calculates voice parameters (rate, volume) based on emotion config
    and adjusted intensity level.
    
    Parameters
    ----------
    emotion : str
        Detected emotion ("joy", "sadness", etc.)
    intensity : float
        Boosted intensity value [0.0, 1.0]
    
    Returns
    -------
    dict with keys: rate (int), volume (float), voice_index (int)
    """
    config = VOICE_CONFIG.get(emotion, VOICE_CONFIG["neutral"])

    rate = config["rate"] + int(config["rate_scale"] * intensity)
    volume = config["volume"] + (config["volume_scale"] * intensity)

    # Safety clamps
    rate = max(80, min(300, rate))
    volume = max(0.5, min(1.0, volume))

    return {
        "rate": int(rate),
        "volume": volume,
        "voice_index": config["voice_index"]
    }

# ─────────────────────────────────────────────────────────────
# 🔹 NATURAL TEXT REWRITING (CONTROLLED + AUTHENTIC)
# ─────────────────────────────────────────────────────────────

def rewrite_text(text: str, emotion: str, intensity: float) -> str:
    """
    Returns the original text as-is without any modifications.
    
    Parameters
    ----------
    text : str
        Original input text
    emotion : str
        Detected emotion
    intensity : float
        Boosted intensity [0.0, 1.0]
    
    Returns
    -------
    str
        Original unchanged text (ready for TTS)
    """
    return text