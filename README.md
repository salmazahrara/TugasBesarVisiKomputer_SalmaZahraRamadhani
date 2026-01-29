# 🎓 Learning Analytics System

**AI-Powered Learning Activity Monitoring menggunakan Computer Vision**

Sistem monitoring pembelajaran real-time yang mendeteksi 4 kondisi mahasiswa: Fokus, Terdistraksi (memegang HP), Mengantuk (diam >6 detik), dan Tidak Ada Aktivitas (tidak terdeteksi webcam).

## 🌟 Features

### 1. Real-time Monitoring (`monitor.py`)
- **YOLOv8 Object Detection** - Deteksi person & cell phone
- **Motion Detection** - Identifikasi kondisi mengantuk
- **Pomodoro Timer** - Integrasi 25/5 menit
- **Live Visualization** - Status real-time di webcam
- **CSV Logging** - Otomatis catat semua aktivitas

### 2. Statistical Analysis (`analyst.py`)
- **Multi-level Aggregation** - Per jam, harian, mingguan
- **Enhanced Visualizations** - 3 chart dengan dark theme
- **Pattern Detection** - Identifikasi jam produktif & rawan
- **Recommendations** - Saran waktu belajar optimal

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt