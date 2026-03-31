from flask import Flask, render_template, request, jsonify
import requests
import json
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

app = Flask(__name__)

# Language mapping - using ISO 639-1 codes for the Translator library
LANGUAGE_MAP = {
    'en': 'en',
    'hi': 'hi',
    'te': 'te',
    'ta': 'ta',
    'kn': 'kn',
    'ml': 'ml',
    'fr': 'fr',
    'es': 'es',
    'de': 'de',
    'ja': 'ja',
    'zh': 'zh',
    'pt': 'pt',
    'ru': 'ru',
    'ar': 'ar',
    'bn': 'bn',
    'gu': 'gu',
    'mr': 'mr',
    'pa': 'pa',
    'ur': 'ur',
}

# Language display names
LANGUAGE_NAMES = {
    'en': 'English',
    'hi': 'Hindi',
    'te': 'Telugu',
    'ta': 'Tamil',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'fr': 'French',
    'es': 'Spanish',
    'de': 'German',
    'ja': 'Japanese',
    'zh': 'Chinese',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ar': 'Arabic',
    'bn': 'Bengali',
    'gu': 'Gujarati',
    'mr': 'Marathi',
    'pa': 'Punjabi',
    'ur': 'Urdu',
}

is_ready = True

@app.route('/status')
def status():
    return jsonify({'ready': is_ready})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/languages')
def get_languages():
    """Return list of supported languages"""
    languages = []
    for code, name in LANGUAGE_NAMES.items():
        languages.append({'code': code, 'name': name})
    return jsonify({
        'supported_languages': languages,
        'note': 'Now with TRUE Telugu support!'
    })

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text', '')
    src_lang = data.get('src_lang', 'en')
    tgt_lang = data.get('tgt_lang', 'hi')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Get language codes
    src_lang_code = LANGUAGE_MAP.get(src_lang)
    tgt_lang_code = LANGUAGE_MAP.get(tgt_lang)
    
    if not src_lang_code or not tgt_lang_code:
        return jsonify({'error': f'Unsupported language code. Source: {src_lang}, Target: {tgt_lang}'}), 400

    try:
        # Use direct Google Translate API
        translated_text = translate_via_google(text, src_lang_code, tgt_lang_code)
        return jsonify({'translated_text': translated_text})
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return jsonify({'error': f'Translation failed: {str(e)}'}), 500

def translate_via_google(text, src_lang, tgt_lang):
    """Direct translation using Google Translate API via requests"""
    try:
        # Method 1: Try using Google Translate API
        url = "https://translate.googleapis.com/translate_a/element.js"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Try the simple translate API endpoint
        endpoint = f"https://translate.google.com/translate_a/single"
        params = {
            'client': 'gtx',
            'sl': src_lang,
            'tl': tgt_lang,
            'dt': 't',
            'q': text
        }
        
        response = requests.get(endpoint, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            # Parse the response - it returns a JSON-like structure
            import re
            # The first element of the array contains the translation
            result = response.json()
            if result and isinstance(result,list) and len(result) > 0:
                translation = result[0][0][0] if result[0] and result[0][0] else text
                return translation
        
        return text
    except Exception as e:
        print(f"Google API error: {e}")
        return text

if __name__ == '__main__':
    print("Starting LinguistAI with TRUE Telugu support!")
    print("Supported languages: English, Hindi, Telugu, Tamil, Kannada, Malayalam, and more!")
    app.run(debug=False, port=5000, host='0.0.0.0')
