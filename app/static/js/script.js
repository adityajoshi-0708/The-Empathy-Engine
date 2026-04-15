/* ═══════════════════════════════════════════════════════════════════════════
   Empathy Engine – JavaScript Frontend Logic
   Handles UI interactions, API calls, and dynamic updates
   ═══════════════════════════════════════════════════════════════════════════ */

// ─────────────────────────────────────────────────────────────────────────── 
// DOM Elements
// ─────────────────────────────────────────────────────────────────────────── 

const textInput = document.getElementById('text-input');
const charCount = document.getElementById('char-count');
const generateBtn = document.getElementById('generate-btn');
const resetBtn = document.getElementById('reset-btn');
const loadingDiv = document.getElementById('loading');
const resultsSection = document.getElementById('results');
const errorSection = document.getElementById('error');
const errorMessage = document.getElementById('error-message');
const errorCloseBtn = document.getElementById('error-close');

const emotionBadge = document.getElementById('emotion-badge');
const intensityValue = document.getElementById('intensity-value');
const intensityLevel = document.getElementById('intensity-level');
const intensityFill = document.getElementById('intensity-fill');
const audioPlayer = document.getElementById('audio-player');
const rewrittenText = document.getElementById('rewritten-text');
const rateValue = document.getElementById('rate-value');
const volumeValue = document.getElementById('volume-value');

// ─────────────────────────────────────────────────────────────────────────── 
// Preset Examples Data
// ─────────────────────────────────────────────────────────────────────────── 

const PRESET_EXAMPLES = {
    happy: "I just won the lottery! This is absolutely amazing and I'm so thrilled! I love this so much!",
    sad: "I can't believe they left me alone. Everything feels so empty and hopeless right now.",
    angry: "This is completely unacceptable! I'm absolutely furious about what just happened!"
};

// Emotion to color mapping
const EMOTION_COLORS = {
    'joy': '#f5576c',
    'anger': '#fa709a',
    'sadness': '#00f2fe',
    'fear': '#a8edea',
    'surprise': '#ffc837',
    'neutral': '#999'
};

// ─────────────────────────────────────────────────────────────────────────── 
// Event Listeners
// ─────────────────────────────────────────────────────────────────────────── 

// Update character count
textInput.addEventListener('input', () => {
    charCount.textContent = textInput.value.length;
});

// Generate button click
generateBtn.addEventListener('click', handleGenerateSpeech);

// Reset button click
resetBtn.addEventListener('click', resetUI);

// Error close button
errorCloseBtn.addEventListener('click', () => {
    errorSection.style.display = 'none';
});

// Preset example buttons
document.querySelectorAll('.example-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        const emotion = e.currentTarget.getAttribute('data-emotion');
        textInput.value = PRESET_EXAMPLES[emotion];
        charCount.textContent = textInput.value.length;
        // Scroll to input
        textInput.focus();
    });
});

// Enter key to generate (Ctrl+Enter for textarea)
textInput.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        handleGenerateSpeech();
    }
});

// ─────────────────────────────────────────────────────────────────────────── 
// Main Functions
// ─────────────────────────────────────────────────────────────────────────── 

/**
 * Handle Generate Speech button click
 */
async function handleGenerateSpeech() {
    const text = textInput.value.trim();

    // Validation
    if (!text) {
        showError('Please enter some text before generating speech.');
        return;
    }

    if (text.length > 500) {
        showError('Text is too long. Maximum 500 characters allowed.');
        return;
    }

    // Disable button and show loading
    generateBtn.disabled = true;
    loadingDiv.style.display = 'flex';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';

    try {
        const response = await fetch('/speak', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to generate speech');
        }

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        console.error('Error:', error);
        showError(`Error: ${error.message}`);
    } finally {
        generateBtn.disabled = false;
        loadingDiv.style.display = 'none';
    }
}

/**
 * Display results in the UI
 */
function displayResults(data) {
    // Update emotion display
    const emotionEmoji = getEmotionEmoji(data.emotion);
    emotionBadge.textContent = `${emotionEmoji} ${capitalize(data.emotion)}`;
    emotionBadge.className = `emotion-badge ${data.emotion}`;
    
    // Update intensity
    const intensityPercent = Math.round(data.intensity * 100);
    intensityValue.textContent = `${intensityPercent}%`;
    intensityLevel.textContent = data.intensity_label;
    intensityFill.style.width = `${intensityPercent}%`;
    
    // Set intensity bar color based on emotion
    const color = EMOTION_COLORS[data.emotion] || '#667eea';
    intensityFill.style.background = `linear-gradient(90deg, ${color} 0%, ${darkenColor(color)} 100%)`;

    // Update audio player
    audioPlayer.src = data.audio_url;

    // Update rewritten text
    rewrittenText.textContent = `"${data.rewritten_text}"`;

    // Update voice parameters
    rateValue.textContent = `${data.rate} WPM`;
    volumeValue.textContent = data.volume.toFixed(2);

    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Reset UI to initial state
 */
function resetUI() {
    textInput.value = '';
    charCount.textContent = '0';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    audioPlayer.src = '';
    generateBtn.disabled = false;
    generateBtn.focus();
}

/**
 * Show error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    errorSection.scrollIntoView({ behavior: 'smooth' });
}

// ─────────────────────────────────────────────────────────────────────────── 
// Utility Functions
// ─────────────────────────────────────────────────────────────────────────── 

/**
 * Get emoji for emotion
 */
function getEmotionEmoji(emotion) {
    const emojiMap = {
        'joy': '😊',
        'anger': '😠',
        'sadness': '😢',
        'fear': '😨',
        'surprise': '😮',
        'neutral': '😐'
    };
    return emojiMap[emotion] || '😊';
}

/**
 * Capitalize first letter
 */
function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * Darken a hex color
 */
function darkenColor(hex) {
    const num = parseInt(hex.replace("#",""), 16);
    const amt = 30;
    const R = Math.min(255, (num >> 16) - amt);
    const G = Math.min(255, (num >> 8 & 0x00FF) - amt);
    const B = Math.min(255, (num & 0x0000FF) - amt);
    return `rgb(${R},${G},${B})`;
}

// ─────────────────────────────────────────────────────────────────────────── 
// Initialize
// ─────────────────────────────────────────────────────────────────────────── 

console.log('🎤 Empathy Engine Frontend Loaded');
textInput.focus();
