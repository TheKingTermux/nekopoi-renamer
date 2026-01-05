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
📝 Judul hasil rename otomatis disimpan ke `judul.txt`  
🔤 `judul.txt` otomatis di-sort alphabetical

---

## 📁 Struktur File

Pastikan file berikut ada di folder yang sama dengan file video NekoPoi anda:

📄 `nekopoi-renamer.ps1`  
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

1️⃣ Jalankan `cleaner.bat` dan skrip akan otomatis rename semua file yang berada di folder yang sama


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

