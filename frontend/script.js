let selectedFile = null;

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
        
        if (!response.ok) throw new Error(`API error! status: ${response.status}`);
        
        const data = await response.json();
        
        // Populate Result Card
        document.getElementById('resClass').textContent = data.name; 
        document.getElementById('resLabel').textContent = data.label;
        
        const confValue = typeof data.confidence === 'number' 
            ? data.confidence.toFixed(2) + '%' 
            : data.confidence;
            
        document.getElementById('resConf').textContent = confValue;
        document.getElementById('resConfText').textContent = confValue;
        
        document.getElementById('resDef').textContent = data.definition;
        document.getElementById('resNut').textContent = data.nutrition;
        document.getElementById('resBen').textContent = data.benefits;

        // Set Emoji based on name
        const emojiMap = {
            "Kedelai Utuh": "🌟",
            "Kedelai Belum Matang": "🌱",
            "Kedelai Kulit Rusak": "🍂",
            "Kedelai Pecah": "💔",
            "Kedelai Bercak": "🍄",
            "Bukan Biji Kedelai": "❓"
        };
        document.getElementById('resEmoji').textContent = emojiMap[data.name] || "🥜";

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
        alert('Gagal menganalisis gambar. Pastikan server backend berjalan.');
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

document.addEventListener('DOMContentLoaded', async () => {
    const badge = document.getElementById('modelStatusBadge');
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        if (data.status === 'ready') {
            badge.textContent = '✅ Model berhasil dimuat';
            badge.style.backgroundColor = '#dcfce7';
            badge.style.color = '#166534';
        } else {
            badge.textContent = '❌ Model gagal dimuat';
            badge.style.backgroundColor = '#fee2e2';
            badge.style.color = '#991b1b';
        }
    } catch (error) {
        badge.textContent = '⚠️ API tidak dapat dihubungi';
        badge.style.backgroundColor = '#fee2e2';
        badge.style.color = '#991b1b';
    }
});
