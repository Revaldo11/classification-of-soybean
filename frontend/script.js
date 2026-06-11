let selectedFile = null;
let modelReady = false;

async function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
        alert('Format file tidak didukung. Silakan gunakan PNG, JPG, atau WEBP.');
        event.target.value = '';
        return;
    }

    selectedFile = file;

    // UI Transitions
    document.getElementById('dropZone').classList.add('hidden');
    document.getElementById('previewContainer').classList.remove('hidden');
    document.getElementById('resultSection').classList.add('hidden');
    
    const imagePreview = document.getElementById('imagePreview');
    const reader = new FileReader();
    reader.onload = function(e) {
        imagePreview.src = e.target.result;
    }
    reader.readAsDataURL(file);
}

async function triggerDetection() {
    if (!selectedFile) return;
    if (!modelReady) {
        alert('Model masih dimuat. Silakan tunggu sampai status model siap.');
        return;
    }

    const loadingSection = document.getElementById('loadingSection');
    const resultSection = document.getElementById('resultSection');
    const btnDetect = document.getElementById('btnDetect');

    loadingSection.classList.remove('hidden');
    resultSection.classList.add('hidden');
    btnDetect.disabled = true;

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            let message = `API error! status: ${response.status}`;
            try {
                const errorData = await response.json();
                message = errorData.detail || message;
            } catch (parseError) {
                // Keep the HTTP status message when the response is not JSON.
            }
            throw new Error(message);
        }
        
        const data = await response.json();
        
        // Populate Result Card
        document.getElementById('resClass').textContent = data.grade; 
        document.getElementById('resLabel').textContent = data.label;
        document.getElementById('resGrade').textContent = data.grade;
        
        const confValue = typeof data.confidence === 'number' 
            ? data.confidence.toFixed(2) + '%' 
            : data.confidence;
            
        document.getElementById('resConf').textContent = confValue;
        document.getElementById('resConfText').textContent = confValue;
        
        document.getElementById('resDef').textContent = data.definition;
        document.getElementById('resNut').textContent = data.nutrition;
        document.getElementById('resBen').textContent = data.benefits;

        // Set Emoji based on grade
        const emojiMap = {
            "Grade A": "🌟",
            "Grade B": "🌱",
            "Grade C": "🍂",
            "Pecah": "💔",
            "Busuk": "🍄",
            "Tidak Terdeteksi": "❓"
        };
        document.getElementById('resEmoji').textContent = emojiMap[data.grade] || "🥜";

        // Progress Bar
        setTimeout(() => {
            const barWidth = typeof data.confidence === 'number' ? data.confidence + '%' : '0%';
            const bar = document.getElementById('resBar');
            bar.style.width = barWidth;
            
            // Change color based on confidence
            if (typeof data.confidence === 'number') {
                if (data.confidence > 85) bar.style.backgroundColor = '#10b981';
                else if (data.confidence > 70) bar.style.backgroundColor = '#3b82f6';
                else bar.style.backgroundColor = '#ef4444';
            }
        }, 100);

        loadingSection.classList.add('hidden');
        resultSection.classList.remove('hidden');
        btnDetect.disabled = false;
        
        // Scroll to results
        resultSection.scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        console.error('Error:', error);
        alert(`Gagal menganalisis gambar. ${error.message}`);
        loadingSection.classList.add('hidden');
        btnDetect.disabled = false;
    }
}

function resetForm() {
    selectedFile = null;
    document.getElementById('fileInput').value = '';
    document.getElementById('cameraInput').value = '';
    closePreview();
}

function closePreview() {
    selectedFile = null;
    document.getElementById('dropZone').classList.remove('hidden');
    document.getElementById('previewContainer').classList.add('hidden');
    document.getElementById('resultSection').classList.add('hidden');
}

function setModelStatusBadge(text, backgroundColor, color) {
    const badge = document.getElementById('modelStatusBadge');
    badge.textContent = text;
    badge.style.backgroundColor = backgroundColor;
    badge.style.color = color;
}

async function fetchWithTimeout(url, timeoutMs = 5000) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

    try {
        const response = await fetch(url, { signal: controller.signal });
        return response;
    } finally {
        clearTimeout(timeoutId);
    }
}

async function checkModelStatus() {
    const maxAttempts = 30;
    const retryDelayMs = 2000;

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        try {
            const response = await fetchWithTimeout('/api/status');
            if (!response.ok) throw new Error(`API error! status: ${response.status}`);

            const data = await response.json();

            if (data.status === 'ready') {
                modelReady = true;
                setModelStatusBadge('✅ Model berhasil dimuat', '#dcfce7', '#166534');
                return;
            }

            if (data.status === 'error') {
                modelReady = false;
                setModelStatusBadge('❌ Model gagal dimuat', '#fee2e2', '#991b1b');
                return;
            }

            setModelStatusBadge('⏳ Model sedang dimuat...', '#fef3c7', '#92400e');
        } catch (error) {
            modelReady = false;
            setModelStatusBadge('⚠️ Menghubungkan ke API...', '#fef3c7', '#92400e');
        }

        await new Promise(resolve => setTimeout(resolve, retryDelayMs));
    }

    setModelStatusBadge('⚠️ API/model belum siap. Coba muat ulang halaman.', '#fee2e2', '#991b1b');
}

document.addEventListener('DOMContentLoaded', () => {
    checkModelStatus();
});
