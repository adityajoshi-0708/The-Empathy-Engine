# 🎤 Empathy Engine – AI with Human Voice

A production-ready web application that detects emotion from text and generates expressive speech with emotional modulation. Perfect for impressing judges in a 30-second demo!

---

## 🎯 Features

✅ **Emotion Detection** — Classifies text into 6 emotion categories (joy, anger, sadness, fear, surprise, neutral)  
✅ **Dynamic Voice Modulation** — Adjusts speech rate, volume, and voice based on detected emotion  
✅ **Human-Touch Enhancement** — Rewrites text with pauses, emphasis, and emotional fillers  
✅ **Beautiful UI** — Color-coded emotion display, real-time feedback, preset examples  
✅ **Fast & Lightweight** — No heavy ML models, offline TTS, <3 seconds generation  
✅ **Mobile-Responsive** — Works perfectly on desktop, tablet, and mobile devices  
✅ **Production-Ready** — Deployment-ready with FastAPI + Render compatibility  

---

## 🏗️ Project Structure

```
DarvixAI_Assement/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI backend
│   ├── emotion.py           # Emotion detection logic
│   ├── voice.py             # TTS and voice modulation
│   ├── config.py            # Voice profiles & text rewriters
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Beautiful, responsive styling
│   │   ├── js/
│   │   │   └── script.js    # Frontend interactivity
│   │   └── audio/           # Generated audio files (auto-created)
│   └── templates/
│       └── index.html       # Main frontend page
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Open in Browser
Navigate to: `http://localhost:8000`

---

## 📝 How It Works

### 1. **Emotion Detection**
- User enters text in the input box
- Text is sent to the `/speak` endpoint
- Transformers model classifies emotion with confidence score
- Edge cases (e.g., "disgust") are mapped to similar emotions (e.g., "anger")

### 2. **Voice Parameter Calculation**
Based on detected emotion and intensity:
- **Joy** → Fast (195 WPM), Energetic, Female voice
- **Anger** → Rapid (175 WPM), Forceful, Male voice  
- **Sadness** → Slow (110 WPM), Soft volume, Female voice
- **Fear** → Hurried (165 WPM), Slightly soft, Female voice
- **Surprise** → Quick (200 WPM), Energetic, Female voice
- **Neutral** → Balanced (150 WPM), Standard tone, Male voice

### 3. **Text Enhancement**
- Dynamic rewriting based on emotion and intensity
- Adds pauses ("..."), emphasis (CAPS), and exclamations
- Example: "I love this" → "Oh wow! I LOVE this! ... That's just AMAZING!"

### 4. **Speech Generation**
- pyttsx3 generates `.wav` file offline
- Parameters applied: rate, volume, voice selection
- File saved to `/app/static/audio/`

### 5. **Frontend Display**
- Shows detected emotion with emoji and color
- Displays intensity level (Low/Medium/High) with visual bar
- Plays generated audio in browser
- Shows voice parameters applied (rate, volume)

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | FastAPI (Python) |
| **TTS Engine** | pyttsx3 (offline) |
| **Emotion Detection** | Transformers (RoBERTa-based) |
| **Frontend** | HTML5 + CSS3 + Vanilla JS |
| **Server** | Uvicorn (ASGI) |
| **Deployment** | Render / Docker |

---

## 📄 Files Overview

### Backend Files
- **`app/main.py`** — FastAPI app with `/speak` endpoint, static file serving
- **`app/emotion.py`** — Emotion classification using Transformers
- **`app/voice.py`** — TTS generation with parameter modulation
- **`app/config.py`** — Voice profiles, text rewriters, emotion configurations

### Frontend Files
- **`app/templates/index.html`** — Main UI page (responsive, accessible)
- **`app/static/css/style.css`** — Beautiful gradient styling, animations
- **`app/static/js/script.js`** — Event handling, API calls, DOM updates

---

## 🎓 Learning Outcomes

This project demonstrates:
- **Emotion Analysis** — Using pre-trained NLP models
- **Voice Synthesis** — TTS with dynamic parameter modulation
- **Full-Stack Development** — Backend API + Frontend UI
- **Production Deployment** — Cloud-ready architecture
- **UX Design** — Color psychology, responsive design
- **Performance Optimization** — Lightweight, offline-first approach

---

## 📝 License

This project is provided as-is for demonstration and educational purposes.

---

## 🎤 Credits

**Empathy Engine** — AI with Human Voice  
Built with ❤️ using FastAPI, pyttsx3, and Transformers

---

**Ready to impress? Open `http://localhost:8000` and start generating expressive speech!** 🚀
