import pandas as pd
import matplotlib.pyplot as plt

# ===============================
# BACA DATA
# ===============================
try:
    df = pd.read_csv("activity_log.csv")
except FileNotFoundError:
    print("❌ File activity_log.csv tidak ditemukan")
    exit()

# ===============================
# BERSIHKAN DATA
# ===============================
df = df[df["timestamp"] != "timestamp"]
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.dropna(subset=["timestamp", "status"])

# ===============================
# EKSTRAK JAM
# ===============================
df["hour"] = df["timestamp"].dt.hour

# ===============================
# REKAP AKTIVITAS
# ===============================
summary = df.groupby(["hour", "status"]).size().unstack(fill_value=0)

# ===============================
# VISUALISASI
# ===============================
summary.plot(kind="bar", figsize=(12, 5))
plt.title("Analisis Aktivitas Mahasiswa per Jam")
plt.xlabel("Jam")
plt.ylabel("Jumlah Aktivitas")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# ===============================
# ANALISIS MENGANTUK
# ===============================
if "Mengantuk" in summary.columns and summary["Mengantuk"].sum() > 0:
    sleepy_hour = summary["Mengantuk"].idxmax()
    print(f"⚠️ Jam rawan mengantuk: {sleepy_hour}:00 – {sleepy_hour+1}:00")
    print("💡 Disarankan tidak menjadwalkan sesi belajar berat di jam ini.")
else:
    print("✅ Tidak ada data aktivitas 'Mengantuk' yang terdeteksi.")
