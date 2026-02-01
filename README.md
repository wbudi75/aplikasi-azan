# 🕌 Python Azan CLI Reminder

Aplikasi pengingat waktu sholat berbasis **CLI (Command Line Interface)** yang ringan dan efisien untuk pengguna Linux. Script ini tidak hanya menampilkan jadwal sholat, tetapi juga memberikan peringatan dini sebelum waktu sholat tiba dan memutar azan secara otomatis.

## ✨ Fitur Utama
- 📅 **Real-time Schedule**: Mengambil data jadwal sholat akurat dari API Aladhan sesuai lokasi (Balikpapan, Indonesia).
- 🔔 **Early Warning System**: Notifikasi pop-up sistem 15 menit sebelum waktu sholat tiba untuk persiapan (Wudhu/ke Masjid).
- 🔊 **Auto Azan Playback**: Memutar audio azan secara otomatis saat memasuki waktu sholat.
- 🎨 **Visual Countdown**: Tampilan terminal yang informatif dengan warna ANSI dan fitur countdown ke waktu sholat berikutnya.
- 🐧 **Native Linux Integration**: Memanfaatkan alat bawaan Linux (`notify-send` & `ffplay`) sehingga sangat ringan tanpa beban library berat.

## 🛠️ Prasyarat (Dependencies)
Script ini dirancang untuk distro berbasis Debian/Ubuntu (termasuk Kali Linux). Pastikan kamu sudah menginstal paket berikut:
sudo apt update
sudo apt install python3-requests python3-dateutil ffmpeg libnotify-bin -y

## 🚀 Cara Instalasi & Penggunaan

1. **Clone Repository**:
git clone [https://github.com/wbudi75/aplikasi-azan.git](https://github.com/wbudi75/aplikasi-azan.git)
cd aplikasi-azan
2. **Siapkan File Audio**:
Pastikan file azan kamu berada di folder `sounds/azan.mp3`.
3. **Jalankan Aplikasi**:
python3 azan.py

## 📂 Struktur Project
aplikasi-azan/
├── azan.py           # Script utama logic Python
├── sounds/
│   └── azan.mp3      # File audio azan
└── README.md         # Dokumentasi project

## ⚙️ Kustomisasi

Kamu bisa mengubah variabel di bagian **CONFIG** pada file `azan.py`:

* `CITY`: Ubah ke kota tempat tinggalmu.
* `NEAR_MINUTES`: Durasi peringatan dini (default 15 menit).

---

*Dibuat dengan Python untuk mempermudah ibadah di tengah kesibukan coding.*



