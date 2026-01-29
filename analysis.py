"""
Learning Analytics - Enhanced Analyst
Analisis aktivitas pembelajaran dengan visualisasi yang lebih baik
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# ===============================
# CONFIGURATION
# ===============================
LOG_FILE = "activity_log.csv"
OUTPUT_DIR = "reports"

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===============================
# LOAD & PROCESS DATA
# ===============================
print("=" * 70)
print("📊 LEARNING ANALYTICS - ENHANCED ANALYST")
print("=" * 70)

try:
    df = pd.read_csv(LOG_FILE)
    print(f"\n✅ Data berhasil dimuat: {LOG_FILE}")
except FileNotFoundError:
    print(f"❌ File {LOG_FILE} tidak ditemukan")
    print("💡 Jalankan monitor.py terlebih dahulu untuk generate data")
    exit()

# Clean data
df = df[df["timestamp"] != "timestamp"]
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.dropna(subset=["timestamp", "status"])

print(f"📄 Total data points: {len(df)}")
print(f"📅 Periode: {df['timestamp'].min()} - {df['timestamp'].max()}")

# Extract time components
df["hour"] = df["timestamp"].dt.hour
df["date"] = df["timestamp"].dt.date
df["day_name"] = df["timestamp"].dt.day_name()

# ===============================
# AGGREGATE DATA
# ===============================
print("\n🔄 Memproses data...")

hourly = df.groupby(["hour", "status"]).size().unstack(fill_value=0)
daily = df.groupby(["date", "status"]).size().unstack(fill_value=0)
weekly = df.groupby(["day_name", "status"]).size().unstack(fill_value=0)

# Reorder days
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekly = weekly.reindex([d for d in day_order if d in weekly.index])

# ===============================
# GENERATE ENHANCED CHARTS
# ===============================
print("\n📈 Membuat visualisasi...")

plt.style.use('dark_background')

# 1. Enhanced Hourly Activity Chart
fig, ax = plt.subplots(figsize=(14, 7))
hourly.plot(kind='bar', ax=ax, color=['#4CAF50', '#FF5252', '#FFC107', '#2196F3'], width=0.8)
ax.set_title('📊 Analisis Aktivitas Mahasiswa per Jam', fontsize=20, fontweight='bold', pad=20)
ax.set_xlabel('Jam', fontsize=14, fontweight='bold')
ax.set_ylabel('Jumlah Aktivitas', fontsize=14, fontweight='bold')
ax.legend(title='Status', fontsize=11, title_fontsize=12)
ax.grid(axis='y', alpha=0.3, linestyle='--')
plt.xticks(rotation=0, fontsize=11)
plt.yticks(fontsize=11)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/hourly_chart.png", dpi=150, facecolor='#1e1e1e')
plt.close()
print("  ✅ hourly_chart.png")

# 2. Enhanced Daily Trend Chart
fig, ax = plt.subplots(figsize=(14, 7))
daily.plot(kind='area', ax=ax, alpha=0.7, color=['#4CAF50', '#FF5252', '#FFC107', '#2196F3'])
ax.set_title('📈 Tren Aktivitas Harian', fontsize=20, fontweight='bold', pad=20)
ax.set_xlabel('Tanggal', fontsize=14, fontweight='bold')
ax.set_ylabel('Jumlah Aktivitas', fontsize=14, fontweight='bold')
ax.legend(title='Status', fontsize=11, title_fontsize=12)
ax.grid(axis='y', alpha=0.3, linestyle='--')
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=11)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/daily_chart.png", dpi=150, facecolor='#1e1e1e')
plt.close()
print("  ✅ daily_chart.png")

# 3. Enhanced Weekly Pattern Chart
fig, ax = plt.subplots(figsize=(12, 7))
weekly.plot(kind='bar', ax=ax, color=['#4CAF50', '#FF5252', '#FFC107', '#2196F3'], width=0.75)
ax.set_title('📅 Pola Aktivitas per Hari (Mingguan)', fontsize=20, fontweight='bold', pad=20)
ax.set_xlabel('Hari', fontsize=14, fontweight='bold')
ax.set_ylabel('Jumlah Aktivitas', fontsize=14, fontweight='bold')
ax.legend(title='Status', fontsize=11, title_fontsize=12)
ax.grid(axis='y', alpha=0.3, linestyle='--')
plt.xticks(rotation=45, fontsize=11)
plt.yticks(fontsize=11)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/weekly_chart.png", dpi=150, facecolor='#1e1e1e')
plt.close()
print("  ✅ weekly_chart.png")

# ===============================
# STATISTICAL ANALYSIS
# ===============================
print("\n" + "=" * 70)
print("📊 ANALISIS STATISTIK")
print("=" * 70)

analysis_lines = []
analysis_lines.append("=" * 70)
analysis_lines.append("LEARNING ANALYTICS - ANALYSIS REPORT")
analysis_lines.append("=" * 70)
analysis_lines.append(f"\n📄 Total Data Points: {len(df)}")
analysis_lines.append(f"📅 Periode Analisis: {df['timestamp'].min()} - {df['timestamp'].max()}\n")

# Overall statistics
print(f"\n📊 Ringkasan Aktivitas:")
for status in hourly.columns:
    total = hourly[status].sum()
    percentage = (total / len(df)) * 100
    print(f"  • {status}: {total} kali ({percentage:.1f}%)")
    analysis_lines.append(f"{status}: {total} kali ({percentage:.1f}%)")

# Peak productivity hour
if "Fokus" in hourly.columns and hourly["Fokus"].sum() > 0:
    peak_hour = hourly["Fokus"].idxmax()
    peak_value = hourly["Fokus"].max()
    print(f"\n🎯 JAM PALING PRODUKTIF")
    print(f"  ⏰ Jam {peak_hour}:00 - {peak_hour+1}:00")
    print(f"  📊 Total fokus: {peak_value} aktivitas")
    print(f"  💡 Rekomendasi: Jadwalkan tugas penting di jam ini")
    
    analysis_lines.append(f"\n🎯 JAM PALING PRODUKTIF: {peak_hour}:00 ({peak_value} aktivitas fokus)")
    analysis_lines.append("💡 Jadwalkan tugas penting di jam ini")

# Sleepy hours analysis
if "Mengantuk" in hourly.columns and hourly["Mengantuk"].sum() > 0:
    sleepy_hour = hourly["Mengantuk"].idxmax()
    sleepy_value = hourly["Mengantuk"].max()
    print(f"\n😴 JAM RAWAN MENGANTUK")
    print(f"  ⏰ Jam {sleepy_hour}:00 - {sleepy_hour+1}:00")
    print(f"  📊 Kejadian mengantuk: {sleepy_value} kali")
    print(f"  ⚠️  Hindari jadwalkan sesi belajar berat di jam ini")
    
    analysis_lines.append(f"\n😴 JAM RAWAN MENGANTUK: {sleepy_hour}:00 ({sleepy_value} kejadian)")
    analysis_lines.append("⚠️  Hindari jadwalkan sesi belajar berat di jam ini")

# Distraction patterns
if "Terdistraksi" in hourly.columns and hourly["Terdistraksi"].sum() > 0:
    distracted_hour = hourly["Terdistraksi"].idxmax()
    distracted_value = hourly["Terdistraksi"].max()
    total_distracted = hourly["Terdistraksi"].sum()
    print(f"\n📱 POLA DISTRAKSI")
    print(f"  ⏰ Jam paling sering terdistraksi: {distracted_hour}:00")
    print(f"  📊 Frekuensi: {distracted_value} kali di jam tersebut")
    print(f"  📊 Total distraksi: {total_distracted} kali")
    print(f"  💡 Saran: Matikan notifikasi HP atau taruh HP jauh di jam ini")
    
    analysis_lines.append(f"\n📱 POLA DISTRAKSI: Jam {distracted_hour}:00 paling sering ({distracted_value} kali)")
    analysis_lines.append(f"Total distraksi: {total_distracted} kali")
    analysis_lines.append("💡 Matikan notifikasi HP atau taruh HP jauh saat belajar")

# Weekly productivity patterns
if not weekly.empty and 'Fokus' in weekly.columns:
    best_day = weekly['Fokus'].idxmax()
    best_day_value = weekly['Fokus'].max()
    worst_day = weekly['Fokus'].idxmin()
    worst_day_value = weekly['Fokus'].min()
    
    print(f"\n🗓️  POLA MINGGUAN")
    print(f"  ✅ Hari paling produktif: {best_day} ({best_day_value} fokus)")
    print(f"  ⚠️  Hari kurang produktif: {worst_day} ({worst_day_value} fokus)")
    
    analysis_lines.append(f"\n🗓️  Hari paling produktif: {best_day} ({best_day_value} fokus)")
    analysis_lines.append(f"Hari kurang produktif: {worst_day} ({worst_day_value} fokus)")

# ===============================
# GENERATE RECOMMENDATIONS
# ===============================
print(f"\n✨ REKOMENDASI WAKTU BELAJAR OPTIMAL")

# Find top 3 productive hours
if "Fokus" in hourly.columns:
    top_hours = hourly["Fokus"].nlargest(3)
    print(f"\n  🕐 Top 3 Jam Terbaik:")
    for i, (hour, value) in enumerate(top_hours.items(), 1):
        print(f"    {i}. Jam {hour}:00 - {hour+1}:00 ({value} aktivitas fokus)")
    
    analysis_lines.append("\n✨ TOP 3 JAM BELAJAR OPTIMAL:")
    for i, (hour, value) in enumerate(top_hours.items(), 1):
        analysis_lines.append(f"  {i}. Jam {hour}:00-{hour+1}:00 ({value} fokus)")

# Avoid hours
avoid_hours = []
if "Mengantuk" in hourly.columns:
    sleepy_hours = hourly[hourly["Mengantuk"] > hourly["Mengantuk"].mean()]
    if not sleepy_hours.empty:
        avoid_hours.extend(sleepy_hours.index.tolist())

if "Terdistraksi" in hourly.columns:
    distracted_hours = hourly[hourly["Terdistraksi"] > hourly["Terdistraksi"].mean()]
    if not distracted_hours.empty:
        avoid_hours.extend(distracted_hours.index.tolist())

if avoid_hours:
    avoid_hours = list(set(avoid_hours))[:3]  # Top 3 to avoid
    print(f"\n  ⛔ Jam yang Sebaiknya Dihindari:")
    for hour in sorted(avoid_hours):
        print(f"    • Jam {hour}:00 - {hour+1}:00")
    
    analysis_lines.append("\n⛔ JAM YANG SEBAIKNYA DIHINDARI:")
    for hour in sorted(avoid_hours):
        analysis_lines.append(f"  • Jam {hour}:00-{hour+1}:00")

# ===============================
# SAVE ANALYSIS REPORT
# ===============================
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
analysis_file = f"{OUTPUT_DIR}/analysis_{timestamp}.txt"

with open(analysis_file, "w", encoding="utf-8") as f:
    f.write("\n".join(analysis_lines))
    f.write("\n\n" + "=" * 70)
    f.write("\nChart visualizations saved in reports/ folder:")
    f.write("\n  • hourly_chart.png - Aktivitas per jam")
    f.write("\n  • daily_chart.png - Tren harian")
    f.write("\n  • weekly_chart.png - Pola mingguan")
    f.write("\n" + "=" * 70 + "\n")

print(f"\n💾 Analisis tersimpan: {analysis_file}")

# ===============================
# DISPLAY SUMMARY
# ===============================
print("\n" + "=" * 70)
print("✨ ANALISIS SELESAI!")
print("=" * 70)
print(f"\n📁 Output tersimpan di folder: {OUTPUT_DIR}/")
print("  📊 3 Chart PNG")
print("  📄 1 Analysis Report TXT")
print("\n💡 Buka file-file tersebut untuk melihat hasil analisis lengkap")
print("=" * 70)