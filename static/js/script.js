document.addEventListener('DOMContentLoaded', () => {
    const srcLang = document.getElementById('src-lang');
    const tgtLang = document.getElementById('tgt-lang');
    const swapBtn = document.getElementById('swap-langs');
    const translateBtn = document.getElementById('translate-btn');
    const sourceText = document.getElementById('source-text');
    const targetText = document.getElementById('target-text');
    const charCount = document.getElementById('char-count');
    const clearBtn = document.getElementById('clear-text');
    const copyBtn = document.getElementById('copy-text');
    const speakBtn = document.getElementById('speak-text');
    const loadingOverlay = document.getElementById('loading-overlay');
    const loadingMsg = loadingOverlay.querySelector('p');

    // Check model status
    async function checkStatus() {
        try {
            const response = await fetch('/status');
            const data = await response.json();
            if (data.ready) {
                translateBtn.disabled = false;
                translateBtn.classList.remove('loading-state');
                translateBtn.querySelector('span').textContent = 'Translate';
            } else {
                translateBtn.disabled = true;
                translateBtn.classList.add('loading-state');
                translateBtn.querySelector('span').textContent = 'Initializing Model...';
                setTimeout(checkStatus, 3000); // Check again in 3s
            }
        } catch (e) {
            console.error("Status check failed", e);
        }
    }

    checkStatus();
    sourceText.addEventListener('input', () => {
        const count = sourceText.value.length;
        charCount.textContent = `${count} / 5000`;
        if (count > 5000) {
            charCount.classList.add('error');
        } else {
            charCount.classList.remove('error');
        }
    });

    // Swap languages
    swapBtn.addEventListener('click', () => {
        const tempLang = srcLang.value;
        srcLang.value = tgtLang.value;
        tgtLang.value = tempLang;
        
        const tempText = sourceText.value;
        sourceText.value = targetText.value;
        targetText.value = tempText;
    });

    // Clear text
    clearBtn.addEventListener('click', () => {
        sourceText.value = '';
        targetText.value = '';
        charCount.textContent = '0 / 5000';
    });

    // Copy text
    copyBtn.addEventListener('click', () => {
        if (!targetText.value) return;
        navigator.clipboard.writeText(targetText.value).then(() => {
            const icon = copyBtn.querySelector('i');
            icon.classList.replace('far', 'fas');
            icon.classList.replace('fa-copy', 'fa-check');
            setTimeout(() => {
                icon.classList.replace('fas', 'far');
                icon.classList.replace('fa-check', 'fa-copy');
            }, 2000);
        });
    });

    // Text to Speech
    speakBtn.addEventListener('click', () => {
        if (!targetText.value) return;
        const utterance = new SpeechSynthesisUtterance(targetText.value);
        utterance.lang = tgtLang.value;
        window.speechSynthesis.speak(utterance);
    });

    // Translate logic
    async function translate() {
        const text = sourceText.value.trim();
        if (!text) return;

        loadingOverlay.classList.remove('hidden');
        translateBtn.disabled = true;

        try {
            const response = await fetch('/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    src_lang: srcLang.value,
                    tgt_lang: tgtLang.value
                }),
            });

            const data = await response.json();
            if (data.translated_text) {
                targetText.value = data.translated_text;
            } else if (data.error) {
                alert('Translation Error: ' + data.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during translation.');
        } finally {
            loadingOverlay.classList.add('hidden');
            translateBtn.disabled = false;
        }
    }

    translateBtn.addEventListener('click', translate);

    // Dynamic icon change for Speak button
    window.speechSynthesis.onvoiceschanged = () => {
        // Voices loaded
    };
});
