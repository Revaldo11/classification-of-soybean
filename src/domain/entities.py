from typing import Dict

SOYBEAN_METADATA = {
    "Broken soybeans": {
        "grade": "Pecah",
        "definition": "Biji kedelai yang pecah atau terbelah menjadi bagian-bagian kecil. Kerusakan ini biasanya terjadi selama proses panen atau pengeringan yang kurang optimal.",
        "nutrition": "Protein, Serat, Isoflavon (sedikit berkurang karena oksidasi).",
        "benefits": "Masih dapat digunakan untuk bahan baku pakan ternak atau diolah menjadi tepung kedelai."
    },
    "Immature soybeans": {
        "grade": "Grade B",
        "definition": "Biji kedelai yang dipanen sebelum matang sempurna. Biasanya berwarna kehijauan dan memiliki ukuran yang lebih kecil dari standar.",
        "nutrition": "Klorofil tinggi, Protein, Vitamin A, Vitamin C.",
        "benefits": "Dapat digunakan sebagai edamame (jika masih segar) atau produk olahan nabati lainnya."
    },
    "Intact soybeans": {
        "grade": "Grade A",
        "definition": "Biji kedelai kualitas super yang utuh, bersih, dan matang sempurna. Tidak ada cacat fisik maupun serangan hama.",
        "nutrition": "Protein Tinggi, Omega-3, Kalsium, Magnesium, Zat Besi.",
        "benefits": "Sangat ideal untuk pembuatan tempe, tahu, dan susu kedelai kualitas premium."
    },
    "Skin-damaged soybeans": {
        "grade": "Grade C",
        "definition": "Biji kedelai yang kulit arinya terkelupas atau berkerut, namun bagian dalamnya masih utuh. Sering disebabkan oleh kelembaban udara.",
        "nutrition": "Protein, Karbohidrat Kompleks, Lemak Sehat.",
        "benefits": "Masih layak dikonsumsi untuk olahan rumah tangga atau kecap kedelai."
    },
    "Spotted soybeans": {
        "grade": "Busuk",
        "definition": "Biji kedelai yang memiliki bercak hitam atau cokelat akibat serangan jamur atau serangga. Menandakan penurunan kualitas yang signifikan.",
        "nutrition": "Protein (menurun), mengandung spora jamur (tidak disarankan dikonsumsi langsung).",
        "benefits": "Harus diproses dengan pemanasan tinggi atau dipisahkan dari biji yang sehat."
    },
    "Bukan Biji Kedelai": {
        "grade": "Tidak Terdeteksi",
        "definition": "Gambar yang diupload tidak teridentifikasi sebagai biji kedelai atau memiliki tingkat akurasi yang sangat rendah.",
        "nutrition": "-",
        "benefits": "Silakan coba upload gambar kedelai yang lebih jelas dan fokus."
    }
}

def get_grade(class_name: str) -> str:
    return SOYBEAN_METADATA.get(class_name, {}).get("grade", "-")

def get_metadata(class_name: str) -> Dict[str, str]:
    return SOYBEAN_METADATA.get(class_name, SOYBEAN_METADATA["Bukan Biji Kedelai"])
