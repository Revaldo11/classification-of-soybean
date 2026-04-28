# Soybean Classification Web App

Aplikasi web untuk klasifikasi biji kedelai menggunakan teknologi AI (TensorFlow/Keras) dengan arsitektur FastAPI dan desain modern.

## Prasyarat (Prerequisites)

- **Python**: Versi 3.10.x (Direkomendasikan 3.10.20)
- **Disk Space**: Minimal 2 GB ruang kosong untuk instalasi TensorFlow.

## Instalasi & Persiapan

### 1. Membuat Virtual Environment
Disarankan untuk menggunakan virtual environment agar tidak bentrok dengan library sistem.

```bash
# Membuat environment baru
python3.10 -m venv tf-env

# Mengaktifkan environment
source tf-env/bin/activate  # Untuk Mac/Linux
# tf-env\Scripts\activate   # Untuk Windows
```

### 2. Menginstal Dependensi
Setelah environment aktif, instal library yang dibutuhkan:

```bash
pip install tensorflow pandas fastapi uvicorn python-multipart pillow
```

### 3. File Model & Mapping
Pastikan file berikut ada di direktori utama project:
- `best_model_skenario3.keras` (Model TensorFlow)
- `class_mapping.csv` (Daftar nama kelas)

## Cara Menjalankan Aplikasi

Jalankan perintah berikut di terminal:

```bash
uvicorn main:app --port 8501 --reload
```

Akses aplikasi melalui browser di: `http://localhost:8501`

## Struktur Project

- `main.py`: Entry point aplikasi (FastAPI server).
- `frontend/`: Berisi file UI (HTML, CSS, JS).
- `src/`: Core logic aplikasi dengan Clean Architecture.
  - `src/adapters/`: Adapter untuk model ML (TensorFlow).
  - `src/use_cases/`: Logika bisnis klasifikasi.
  - `src/domain/`: Entitas dan definisi data.
- `patch_model.py`: Script utility untuk memperbaiki masalah kompatibilitas deserialisasi model Keras.
