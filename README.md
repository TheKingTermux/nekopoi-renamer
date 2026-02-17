# 🎬 nekopoi-renamer

🚀 Script PowerShell untuk **merapikan, menstandarkan, dan mengelola** nama file video NekoPoi secara otomatis.  
Cocok buat koleksi gede biar **rapi, konsisten, dan bebas duplikat**. Hidup jadi damai ✨

---

## ✨ Fitur Utama

✅ Rename otomatis file video (.mp4, .mkv, .mov, .webm)  
🧹 Menghapus tag NekoPoi & domain (nekopoi.care, .fun, .tv, dll)  
🪚 Membersihkan simbol berantakan: `[] () _`  
🧠 Deteksi & standarisasi:
- 🎟️ Kode JAV (FC2, SONE, EBWH, dll)
- 📺 Resolusi (480P, 720P, 1080P)
- 🧩 Dimensi (2D, 3D, LIVE2D)

🏷️ Deteksi author / studio otomatis dari `author.txt`  
🔒 Keyword penting tetap kapital (TK, UKS, ZZZ, dll)  
🚫 Anti duplikat:
- Dalam satu sesi
- Global via `judul.txt`

📦 File duplikat otomatis dipindah ke folder `_DUPLICATE`  
📦 File JAV / Live Action otomatis dipindah ke folder `Real`  
📦 File Selain Nekopoi otomatis dipindah ke folder `Lainnya`  
📝 Judul hasil rename otomatis disimpan ke `judul.txt`  
🔤 `judul.txt` otomatis di-sort alphabetical

---

## 📁 Struktur File

Pastikan file berikut ada di folder yang sama dengan file video NekoPoi anda:

📄 `debug.ps1`  
📄 `debug.py`  
📄 `cleaner.py`  
📄 `cleaner.bat`  
📄 `author.txt`  
📄 `keyword.txt`  
📄 `judul.txt`  

---

## 🏷️ author.txt

Daftar author / studio.  
📌 **Satu baris = satu author**

Contoh:
- Horny Herring Studios
- CBX-CJW
- Peh-koi
- Misumi
- MAKODA


---

## 🔑 keyword.txt

Daftar keyword yang **harus tetap kapital** (tidak kena TitleCase).

Contoh:
- TK
- UKS
- ZZZ
- HSR
- UNCENSORED
- FGO


---

## 📚 judul.txt

Database judul yang sudah pernah diproses.  
Dipakai buat **mencegah rename judul duplikat** 🛑

Contoh isi:
- EBWH-063 - U 480P
- SONE-788 Nekpoi - U 480P


---

## 🔄 Contoh Rename

🎯 **Sebelum:**
`[NekoPoi]EBWH-063-U[480p].mp4`


✨ **Sesudah:**
`EBWH-063 - U 480P.mp4`


---

🎯 **Sebelum:**
`NekoPoi_720p_Horny_Herring_Studios_Lyriel_Elf_Maid_from_A_House.mp4`


✨ **Sesudah:**
`Horny Herring Studios - Lyriel Elf Maid From A House 720P.mp4`


---

## 🚨 Perilaku Duplikat

Jika judul:
- 🧠 sudah ada di `judul.txt`, atau
- 👯 muncul dua kali dalam satu proses

Maka file akan:
- ❌ Tidak di-rename
- 📦 Dipindahkan ke folder `_DUPLICATE`
- ⚠️ Diberi peringatan di console

---

## ▶️ Cara Pakai

### 🧠 Auto Install Python (Smart Launcher)

Mulai versi terbaru, `cleaner.bat` sudah dilengkapi **auto dependency checker**.

Jika Python belum terinstall di sistem:

* 🔍 Script akan mendeteksi otomatis
* 🖥️ Auto detect 32-bit / 64-bit Windows
* ⬇️ Mengunduh installer resmi dari python.org
* ⚙️ Silent install (tanpa pop-up)
* 🧹 Installer otomatis dihapus setelah selesai
* ▶️ Script langsung berjalan

📌 File installer hanya disimpan sementara di folder script dan akan otomatis dihapus.
📌 Tidak ada file lain yang dihapus selain installer Python tersebut.

---

## 🏗️ Arsitektur yang Didukung

* ✅ Windows 32-bit
* ✅ Windows 64-bit
* 🔄 Otomatis menyesuaikan versi installer

---

## 🛠️ Menu Launcher

Saat menjalankan `cleaner.bat`, tersedia menu:

1️⃣ Main Script (Python)
2️⃣ Cleaner Mode (Python)
3️⃣ Deprecated PowerShell
4️⃣ Keluar
5️⃣ Install Python Manual

💡 Menu 1 & 2 sudah otomatis melakukan pengecekan Python, jadi biasanya tidak perlu memilih menu 5.

---

## 🔐 Keamanan

Script ini:

* ❌ Tidak menghapus file video
* ❌ Tidak menghapus folder lain
* ❌ Tidak mengubah isi file
* ✅ Hanya rename nama file
* ✅ Memindahkan file duplikat ke `_DUPLICATE`
* ✅ Menghapus **hanya** file installer Python sementara

---

## ⚡ Dependency Management

Launcher bertindak sebagai:

> Lightweight bootstrapper + dependency manager

Artinya pengguna awam pun bisa langsung menjalankan script tanpa perlu install Python manual terlebih dahulu.

---

## 📌 Catatan

ℹ️ Script **hanya mengubah nama file**, bukan isi video  
💪 Aman untuk ribuan file  
🧘 Fokus ke kerapian arsip jangka panjang

---

😌 Koleksi rapi  
😎 Nama konsisten  
🧠 Hidup lebih tenang  

**Happy renaming! 🔥**
