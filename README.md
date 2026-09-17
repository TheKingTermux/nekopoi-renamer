# 🎬 nekopoi-renamer

Python-based automation tool untuk **merapikan, menstandarkan, mengelompokkan, dan mengelola koleksi video NekoPoi & JAV** secara otomatis.

Walaupun namanya `nekopoi-renamer`, script ini pada dasarnya bisa memproses berbagai file video. Fokus utamanya adalah membuat filename lebih konsisten sekaligus memisahkan file berdasarkan kategori, sumber, dan kondisi tertentu.

> ⚠️ **Catatan:** README ini mendokumentasikan perilaku script versi terbaru. Beberapa fitur bergantung pada isi `author.txt`, `keyword.txt`, dan `cosplay.txt` milik pengguna.

---

## ✨ Fitur Utama

### 🎯 Smart Renaming

Mendukung file video:

- `.mp4`
- `.mkv`
- `.mov`
- `.webm`

Script mencoba mengenali bagian penting dari filename, kemudian menyusunnya kembali menjadi format yang konsisten.

Secara umum hasil rename dapat berisi:

```text
[NTR] - [CODE] - [STUDIO/AUTHOR] - [TITLE] - [EPISODE/VOLUME/PART] [UNCENSORED] [RESOLUTION]
```

Bagian yang tidak ditemukan akan dilewati secara otomatis.

---

## 🧠 Automatic Detection

### 🎟️ JAV / Video Code

Script menggunakan daftar pola dan whitelist code untuk menghindari salah deteksi terhadap angka biasa di dalam judul.

Beberapa kelompok code yang didukung antara lain:

- FC2 / FC2-PPV
- SSNI
- SSIS
- DLDSS
- MIAA
- MIDV
- IPX
- STARS
- CAWD
- HMN
- FSDSS
- JUQ
- FOCS
- RCTD
- REAL
- KBJ
- HEYZO
- SIRO
- 1PON
- CARIB
- FPRE
- JDKR
- MDWP
- PMA
- MIAB
- MIDA
- MIMK
- SNOS
- START
- MUDR
- ABF / ABP / ADN / ATID
- BF / BLK / EBOD / EBWH
- GANA / GOPJ / JUR / MEYD
- NIMA / NSFS / PRED
- S-Cute / SUPA / TEK / WANZ / XVSR
- dan beberapa prefix custom lainnya

Selain prefix yang dikenal, pola generic digunakan secara terbatas untuk menangani format code tertentu tanpa menganggap setiap kombinasi huruf + angka sebagai code.

Contoh normalisasi:

```text
ABP123      → ABP-123
FC21234567  → FC2-PPV-1234567
```

> Daftar code sengaja tidak dibuat terlalu bebas karena angka seperti `Episode-12`, `Part-03`, `Season-02`, atau `NTR-01` dapat menyebabkan false positive jika pola dibuat terlalu umum.

---

### 📺 Resolution Detection

Mendeteksi resolution berikut:

- `360P`
- `480P`
- `720P`
- `1080P`
- `1440P`
- `2160P`

Resolution yang ditemukan akan dipindahkan ke bagian akhir filename.

Contoh:

```text
Some Title 1080p.mp4
→ Some Title 1080P.mp4
```

---

### 🔒 UNCENSORED Detection

Mendeteksi penanda seperti:

- `U`
- `UC`
- `UNCEN`
- `UNCENSORED`
- beberapa suffix terkait seperti `LEAK` / `MR` pada code yang mendukungnya

Penanda yang berhasil dikenali dapat digunakan sebagai suffix filename.

---

### 🧩 Dimension Detection

Mendeteksi:

- `2D`
- `3D`
- `LIVE2D`
- `L2D`

Informasi ini digunakan sebagai bagian dari title ketika ditemukan.

---

## 🔞 NTR Detection

Script mempunyai daftar keyword NTR yang cukup luas, termasuk istilah bahasa Inggris dan Indonesia.

Contoh keyword:

```text
ntr
netorare
netori
netorase
cheating
cuckold
cuck
affair
adultery
infidelity
betrayal
unfaithful
side piece
stolen wife
wife sharing
sharing
istri orang
suami orang
selingkuh
selingkuhan
perselingkuhan
pihak ketiga
istri dicuri
berbagi istri
berbagi pasangan
```

Deteksi NTR hanya diperlakukan sebagai prefix ketika keyword ditemukan pada posisi yang sesuai. Kemunculan kata `ntr` di tengah judul tidak otomatis membuat seluruh judul menjadi NTR.

Contoh:

```text
NTR Some Title.mp4
→ NTR - Some Title.mp4
```

Sedangkan judul seperti:

```text
I Made My Girlfriend Love NTR Part.mp4
```

tidak dipotong hanya karena memiliki kata `NTR` di tengah judul.

---

## 👤 Studio / Author Detection

Studio atau author dapat dikenali melalui:

### `author.txt`

Daftar author/studio dapat dikelola melalui file:

```text
author.txt
```

### Format `by StudioName`

Filename dengan pola seperti:

```text
Some Title by StudioName.mp4
```

dapat diproses sebagai informasi studio/author.

Nama author yang baru ditemukan melalui pola `by ...` juga dapat ditambahkan ke `author.txt` ketika script dijalankan dalam mode non-dry-run.

---

## 🧹 Intelligent Cleaning

Sebelum proses rename, script membersihkan berbagai noise dari filename.

Yang ditangani antara lain:

- URL
- domain spam
- domain downloader
- `nekopoi` / variasi penulisan tertentu
- `alqanime`
- bracket `[]`, `{}`, `()`
- underscore
- spasi berulang
- dash berlebihan
- metadata subtitle
- metadata resolution
- metadata uncensored
- code dan studio yang sudah berhasil diekstrak

Domain spam yang dikenali mencakup berbagai TLD umum seperti `.care`, `.fun`, `.tv`, `.id`, `.io`, `.xyz`, `.site`, `.club`, `.live`, dan lainnya.

---

## 🔤 Keyword Preservation

Keyword tertentu dapat dipertahankan menggunakan:

```text
keyword.txt
```

File ini digunakan untuk menentukan keyword yang perlu dipertahankan ketika proses cleaning / normalisasi filename dilakukan.

---

# 🚫 Smart Bypass System

Tidak semua file seharusnya diproses oleh rename engine. Karena itu script mempunyai beberapa **hard bypass**.

File yang terkena hard bypass akan langsung diarahkan ke folder tujuan tanpa masuk ke proses rename normal.

### #️⃣ Hashtag

File yang mengandung `#` akan langsung masuk ke:

```text
Lainnya/
```

Contoh:

```text
Video #tiktok #viral.mp4
→ Lainnya/Video #tiktok #viral.mp4
```

Nama file tetap dipertahankan.

---

### 😀 Emoji / Unicode Symbol

Script mempunyai deteksi emoji/symbol Unicode yang cukup agresif untuk mencegah file dengan emoji lolos ke rename engine.

Jika terdeteksi:

```text
→ Lainnya/
```

Nama file tetap dipertahankan.

---

### 📥 Social Media Downloader

Filename yang mengandung penanda downloader tertentu akan langsung diarahkan ke `Lainnya/`.

Contoh penanda yang dikenali:

- `snapsave`
- `fbdownload`
- `fdownloader`
- `savefrom`
- `fbcdn`
- `ssstik`
- `facebook`

---

### 🇬🇧 English Subtitle

File yang jelas ditandai sebagai English subtitle akan diarahkan ke:

```text
English/
```

Penanda yang dikenali antara lain:

- `english`
- `engsub`
- `engsubs`
- `eng sub`
- `eng subs`
- `subtitle english`
- `subtitle eng`
- `sub eng`
- `sub english`
- `subbed english`
- `subbed eng`
- `v1x`

File English bypass tidak masuk ke rename engine normal.

---

## 🎭 Cosplay Detection

Script mempunyai file konfigurasi khusus:

```text
cosplay.txt
```

Setiap nama yang ditulis di dalam file tersebut dapat digunakan sebagai keyword cosplay.

Jika filename cocok dengan salah satu nama cosplay, file langsung diarahkan ke:

```text
Real/Cosplay/
```

Cosplay diperlakukan sebagai **hard bypass**, sehingga filename tidak diubah oleh rename engine.

Contoh:

```text
Raiden OL Video - Meenfox.mp4
→ Real/Cosplay/Raiden OL Video - Meenfox.mp4
```

Pencocokan menggunakan batas kata agar nama yang hanya menjadi bagian dari kata lain tidak mudah terkena false positive.

---

## 📦 Non-NekoPoi Routing

Setelah hard bypass diproses, file yang tidak memiliki code atau resolution yang dikenali dan juga tidak memenuhi indikator NekoPoi akan diarahkan ke:

```text
Lainnya/
```

Tujuannya agar file random / non-target tidak ikut masuk ke koleksi `Real/`.

---

# 📁 Auto Folder Routing

Folder yang digunakan script:

```text
Real/
Real/Cosplay/
English/
Lainnya/
_DUPLICATE/
_DUPLICATE/Large/
```

Routing utama:

| Kondisi | Tujuan |
|---|---|
| File dengan code valid | `Real/` |
| File cosplay | `Real/Cosplay/` |
| English subtitle | `English/` |
| Hashtag | `Lainnya/` |
| Emoji / symbol | `Lainnya/` |
| Social downloader | `Lainnya/` |
| Non-NekoPoi tanpa config/code | `Lainnya/` |
| Duplicate | `_DUPLICATE/` |
| Duplicate berukuran besar | `_DUPLICATE/Large/` |

Folder yang belum ada akan dibuat otomatis oleh script.

---

# 🧠 Duplicate Detection

Script melakukan pengecekan duplicate berdasarkan title yang telah diproses.

Registry judul disimpan pada:

```text
judul.txt
```

Perbandingan dilakukan secara case-insensitive.

Jika title sudah pernah ditemukan dalam sesi pemrosesan, file berikutnya dapat diarahkan ke:

```text
_DUPLICATE/
```

---

## 📦 Large Duplicate

Duplicate dengan ukuran file besar dipisahkan lagi ke:

```text
_DUPLICATE/Large/
```

Threshold ukuran dikontrol oleh konfigurasi:

```python
LARGE_DUP_SIZE
```

Dengan demikian duplicate biasa dan duplicate berukuran besar tidak tercampur dalam satu folder.

---

# 📝 Title Registry — `judul.txt`

`judul.txt` berfungsi sebagai registry judul.

Kegunaannya meliputi:

- menyimpan title yang sudah diproses
- membantu pengecekan duplicate antar sesi
- perbandingan case-insensitive
- menjaga daftar title tetap persisten
- menghindari pemrosesan ulang title yang sama

---

# 🛠️ Configuration Files

### `author.txt`

Daftar studio / author yang dikenal script.

### `keyword.txt`

Daftar keyword yang perlu dipertahankan saat proses cleaning.

### `cosplay.txt`

Daftar nama / keyword cosplay untuk routing ke `Real/Cosplay/`.

### `judul.txt`

Registry title yang telah diproses.

---

# 🔄 DRY RUN Mode

Script menyediakan mode simulasi:

```python
DRY_RUN = True
```

Dalam mode ini script dapat menampilkan hasil rename dan routing tanpa benar-benar mengubah file di disk.

Untuk menjalankan perubahan sebenarnya:

```python
DRY_RUN = False
```

> Disarankan menjalankan `DRY_RUN = True` terlebih dahulu untuk memeriksa hasil sebelum melakukan rename/move massal.

---

# 🛡️ Safe Move & Collision Handling

Pemindahan file menggunakan mekanisme safe move untuk menangani kondisi ketika nama tujuan sudah ada.

Tujuannya agar proses tidak sembarangan menimpa file yang sudah ada.

Script juga tidak mengubah isi video. Operasinya berfokus pada:

- membaca filename
- rename
- memindahkan file
- mencatat registry / log

---

# 🧪 Debug / Troubleshooting

Repository juga menyediakan file debug untuk membantu investigasi masalah:

```text
debug.py
debug.ps1
```

Gunakan file tersebut ketika ingin memeriksa perilaku parsing atau masalah tertentu tanpa langsung mengubah koleksi utama.

---

# 📂 Struktur Repository

Struktur dasar repository saat ini mencakup:

```text
nekopoi-renamer/
├── cleaner.py
├── cleaner.bat
├── debug.py
├── debug.ps1
├── author.txt
├── keyword.txt
├── cosplay.txt
├── judul.txt
└── README.md
```

> `cosplay.txt` dan file konfigurasi/registry dapat dibuat atau diisi sesuai kebutuhan penggunaan lokal.

---

# 🚀 Cara Penggunaan

1. Letakkan script dan file konfigurasi pada folder kerja yang sesuai.
2. Isi `author.txt`, `keyword.txt`, dan `cosplay.txt` bila diperlukan.
3. Pastikan video yang ingin diproses berada pada folder kerja script.
4. Jalankan dengan:

```python
DRY_RUN = True
```

untuk melihat simulasi terlebih dahulu.

5. Jika hasil sudah sesuai, ubah menjadi:

```python
DRY_RUN = False
```

6. Jalankan kembali script untuk melakukan rename dan move sebenarnya.

---

# 🎯 Contoh

### NekoPoi / JAV

```text
[NekoPoi]_SSNI123_U_1080p.mp4
```

Dapat diproses menjadi format seperti:

```text
SSNI-123 - 1080P.mp4
```

Hasil akhirnya kemudian diarahkan sesuai rule routing script.

---

### NTR

```text
NTR - Some Title 720p.mp4
```

Menjadi title dengan prefix NTR yang tetap dipertahankan dan resolution di bagian akhir.

---

### Cosplay

```text
Raiden OL Video - Meenfox.mp4
```

Jika `Meenfox` terdaftar di `cosplay.txt`:

```text
Real/
└── Cosplay/
    └── Raiden OL Video - Meenfox.mp4
```

Tidak dilakukan rename normal.

---

### Hashtag

```text
Video #tiktok #viral.mp4
```

Hasil:

```text
Lainnya/
└── Video #tiktok #viral.mp4
```

---

### English Subtitle

```text
Some Title ENG SUB 1080p.mp4
```

Jika memenuhi rule English subtitle:

```text
English/
└── Some Title ENG SUB 1080p.mp4
```

---

### Duplicate

Jika title sudah terdeteksi sebagai duplicate:

```text
_DUPLICATE/
└── <filename>
```

Jika ukurannya melewati threshold large duplicate:

```text
_DUPLICATE/
└── Large/
    └── <filename>
```

---

# ⚡ Cocok Untuk

- Koleksi JAV
- Arsip NekoPoi
- Koleksi video besar
- Folder dengan ribuan file
- Storage jangka panjang
- Persiapan media server / library pribadi
- Koleksi yang membutuhkan naming dan folder routing konsisten

---

# ⚠️ Catatan Penting

Script ini bekerja berdasarkan pola filename. Tidak ada parser isi video untuk menentukan isi sebenarnya.

Karena itu:

- false positive tetap mungkin terjadi
- filename yang sangat tidak standar mungkin tidak dikenali
- daftar code sengaja menggunakan whitelist agar angka biasa tidak mudah dianggap sebagai code
- keyword pada `author.txt`, `keyword.txt`, dan `cosplay.txt` memengaruhi hasil
- gunakan `DRY_RUN = True` sebelum menjalankan batch processing pada koleksi besar

---

# 🧘 Philosophy

```text
Minimal manual work.
Less chaos in filenames.
Deterministic organization.
Archive-friendly collection management.
```

---

## 📜 License / Usage

Gunakan dan modifikasi script sesuai kebutuhan pribadi. Pastikan penggunaan script dan koleksi yang diproses tetap sesuai dengan hukum serta ketentuan layanan yang berlaku di wilayah masing-masing.
