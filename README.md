# 📚 Student Learning Activity Monitoring with YOLOv8

Sistem ini merupakan proyek **Computer Vision** untuk memonitor aktivitas belajar mahasiswa secara **real-time** menggunakan kamera. Sistem memanfaatkan **YOLOv8** untuk deteksi objek dan **analisis pergerakan** untuk mengklasifikasikan status belajar mahasiswa.

Status aktivitas belajar yang dapat dikenali:

* 🎯 **Fokus**
* 😴 **Mengantuk**
* 📱 **Terdistraksi**
* 🚫 **Tidak Ada Aktivitas**

Data aktivitas dicatat secara otomatis dan dianalisis untuk memperoleh **pola produktivitas belajar** serta rekomendasi waktu belajar yang optimal.

---

## 👩‍🎓 Informasi Mahasiswa

* **Nama**: Salma Zahra Ramadhani
* **Username GitHub**: salmazahrara
* **Mata Kuliah**: Computer Vision / Artificial Intelligence
* **Konteks**: Tugas Akademik

---

## 🧠 Fitur Utama

* Monitoring aktivitas belajar secara **real-time**
* Deteksi objek **person** dan **cell phone** menggunakan YOLOv8
* Klasifikasi status belajar otomatis
* Pencatatan data aktivitas ke file CSV
* Analisis data dan visualisasi grafik produktivitas

---

## 🛠️ Tools & Teknologi

* **Python 3.11**
* **YOLOv8 (Ultralytics)**
* **OpenCV (cv2)**
* **Pandas**
* **Matplotlib**
* **CSV (Data Logging)**

---

## 📂 Struktur Folder

```
├── monitor.py               # Program utama monitoring real-time
├── analysis.py              # Analisis dan visualisasi data
├── dummy_activity_log.csv   # Contoh data aktivitas (dummy)
├── requirements.txt         # Daftar library Python
├── .gitignore               # File ignore Git
└── README.md                # Dokumentasi proyek
```

---

## ⚙️ Instalasi & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/salmazahrara/nama-repo.git
cd nama-repo
```

### 2️⃣ Install Dependencies

Disarankan menggunakan virtual environment.

```bash
pip install -r requirements.txt
```

Isi `requirements.txt`:

```txt
ultralytics
opencv-python
pandas
matplotlib
```

---

## ▶️ Cara Penggunaan

### 🔹 Menjalankan Sistem Monitoring

Pastikan kamera (webcam) aktif, kemudian jalankan:

```bash
python monitor.py
```

Sistem akan:

* Mendeteksi objek **person** dan **cell phone**
* Menganalisis pergerakan pengguna
* Menampilkan status belajar secara real-time
* Menyimpan data aktivitas ke file CSV

---

### 📌 Logika Klasifikasi Status

| Status              | Kriteria                                       |
| ------------------- | ---------------------------------------------- |
| Fokus               | Person terdeteksi + ada gerakan + tidak ada HP |
| Mengantuk           | Person terdeteksi + diam ≥ 6 detik             |
| Terdistraksi        | HP terdeteksi                                  |
| Tidak Ada Aktivitas | Tidak ada person                               |

---

### 🔹 Analisis Data Aktivitas

Setelah monitoring selesai, jalankan:

```bash
python analysis.py
```

Program akan:

* Membaca file CSV aktivitas
* Melakukan agregasi data berdasarkan waktu
* Menampilkan grafik pola produktivitas belajar

Grafik yang dihasilkan menunjukkan:

* Jam dengan fokus tinggi
* Jam rawan mengantuk
* Jam dengan distraksi tinggi

---

## 📈 Output Sistem

* **File CSV**: Data aktivitas belajar
* **Grafik visualisasi** produktivitas belajar
* **Insight pola belajar mahasiswa**

---

## ⚠️ Keterbatasan Sistem

* Sensitif terhadap kondisi pencahayaan
* Hanya mendukung satu pengguna
* Belum menggunakan deteksi ekspresi wajah atau eye tracking

---

## 🚀 Pengembangan Selanjutnya

* Multi-user detection
* Eye tracking dan face landmark
* Dashboard web interaktif
* Rekomendasi belajar otomatis berbasis *Pomodoro Technique*

---

## 📌 Lisensi & Catatan

Proyek ini dibuat untuk **keperluan edukasi dan penelitian**.
Silakan digunakan dan dikembangkan sesuai kebutuhan pembelajaran.

---

✨ *Dokumentasi ini disusun untuk mendukung penilaian akademik dan publikasi di GitHub.*
