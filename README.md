# 🎬 nekopoi-renamer

🚀 Python-based automation tool untuk **merapikan, menstandarkan, dan mengelola koleksi video NekoPoi & JAV** secara otomatis.

Dirancang untuk koleksi besar agar:

* Rapi
* Konsisten
* Bebas duplikat
* Terstruktur per kategori

---

# ✨ Fitur Utama (Versi Terbaru)

## 🎯 Smart Renaming Engine

* Rename otomatis file video: `.mp4`, `.mkv`, `.mov`, `.webm`
* Format final konsisten:

  ```
  [NTR] - [CODE] - [STUDIO/AUTHOR] - [TITLE] - [EPISODE] [UNCENSORED] [RESO]
  ```

---

## 🧠 Deteksi Otomatis

### 🎟️ Kode JAV

Mendukung:

* FC2-PPV
* SSNI, SSIS, IPX, CAWD, EBWH, dll
* Prefix custom fleksibel
* Auto normalize → `ABP123` → `ABP-123`

### 📺 Resolusi

* 360P
* 480P
* 720P
* 1080P
* 1440P
* 2160P

### 🔒 UNCENSORED Detection

* U
* UC
* UNCEN
* UNCENSORED

### 🧩 Dimensi

* 2D
* 3D
* LIVE2D
* L2D

### 🔞 NTR Detection

Jika filename mengandung:

```
ntr, netorare, netori, netorase,
cheating, cuckold, cuck, affair
```

→ Otomatis ditambahkan prefix:

```
NTR - ...
```

---

## 🏷️ Studio / Author Detection

* Auto detect dari `author.txt`
* Support `by StudioName`
* Jika studio baru ditemukan:

  * Otomatis ditambahkan ke `author.txt`
  * Langsung aktif tanpa restart

---

## 🧹 Intelligent Cleaning

* Hapus domain spam (.care, .fun, .tv, dll)
* Hapus `nekopoi` fleksibel (bahkan typo spacing)
* Bersihkan simbol: `[] {} () _`
* Perbaikan dash berantakan
* Slug URL auto-fix

---

## 🔠 Smart Title Case

* Huruf kapital pintar
* Angka tidak dirusak
* Keyword penting tidak berubah (`keyword.txt`)
* Tidak merusak ALL CAPS yang memang intentional

---

## 🎬 Episode Auto Detection

Jika judul diakhiri angka:

```
Title 1 → Title - 01
```

Kecuali:

```
Season 2
```

---

# 🚫 Smart Bypass System

File berikut **tidak akan di-rename** dan langsung masuk folder `Lainnya`:

### 🔹 File dengan Hashtag (#)

Contoh:

```
Video #tiktok #viral.mp4
```

### 🔹 File Downloader Sosmed

* snapsave
* fbdownload
* savefrom
* fbcdn
* dll

### 🔹 File Non-NekoPoi Tanpa Code/Resolusi

---

# 📦 Auto Folder Routing

| Kondisi               | Tujuan                |
| --------------------- | --------------------- |
| Punya kode JAV        | `Real/`               |
| Duplikat              | `_DUPLICATE/`         |
| Hashtag / Non-NekoPoi | `Lainnya/`            |
| Sisanya               | Tetap di folder utama |

---

# 🧠 Anti Duplikat System

Deteksi:

* Duplikat dalam satu sesi
* Duplikat global via `judul.txt`

Jika terdeteksi:

* Tidak di-rename ulang
* Dipindah ke `_DUPLICATE`
* Dicatat di registry

---

# 📝 Registry System (`judul.txt`)

* Semua judul hasil rename disimpan
* Otomatis disortir alphabetical
* Case-insensitive comparison
* Persisten antar sesi

---

# 🔄 DRY RUN Mode

```python
DRY_RUN = True
```

Test mode:

* Tidak rename
* Tidak move
* Hanya print hasil


```python
DRY_RUN = False
```

Production mode:

* Langsung rename
* Langsung move
* Langsung print hasil

---

# 📁 Struktur File

Pastikan ada:

```
cleaner.py
cleaner.bat
author.txt
keyword.txt
judul.txt
```

---

# 🏗️ Folder Otomatis Dibuat

Jika belum ada, script akan membuat:

```
Real/
_Duplicate/
Lainnya/
```

---

# 🔐 Keamanan

Script ini:

* ❌ Tidak menghapus video
* ❌ Tidak mengubah isi video
* ❌ Tidak menyentuh folder luar
* ✅ Hanya rename
* ✅ Hanya move sesuai rule
* ✅ Safe collision handling

---

# 🎯 Contoh Rename

### Sebelum

```
[NekoPoi]_SSNI123_U_720p.mp4
```

### Sesudah

```
SSNI-123 - U 720P.mp4
```

---

### Sebelum

```
NTR_Yor_720p.mp4
```

### Sesudah

```
NTR - Yor 720P.mp4
```

---

### Sebelum

```
Video #tiktok #viral.mp4
```

### Hasil

Masuk `Lainnya/` tanpa rename

---

# ⚡ Cocok Untuk

* Kolektor JAV
* Arsip NekoPoi besar
* Folder ribuan file
* Storage jangka panjang
* Self-hosted media server prep

---

# 🧘 Philosophy

Minimal manual work.
Zero chaos naming.
Deterministic sorting.
Archive-grade organization.
