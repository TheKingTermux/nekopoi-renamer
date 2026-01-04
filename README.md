# nekopoi-renamer

Script PowerShell untuk merapikan, menstandarkan, dan mengelola nama file video NekoPoi secara otomatis.
Cocok untuk koleksi besar biar rapi, konsisten, dan bebas duplikat.

---

## Fitur Utama

- Rename otomatis file video (.mp4, .mkv, .mov, .webm)
- Menghapus tag NekoPoi dan domain (nekopoi.care, .fun, .tv, dll)
- Membersihkan simbol berantakan seperti [], (), dan _
- Deteksi dan standarisasi:
  - Kode JAV (FC2, SONE, EBWH, dll)
  - Resolusi (480P, 720P, 1080P)
  - Dimensi (2D, 3D, LIVE2D)
- Deteksi author / studio otomatis dari author.txt
- Keyword terlindungi agar tetap kapital (TK, UKS, ZZZ, dll)
- Pencegahan judul duplikat:
  - Dalam satu sesi
  - Global via judul.txt
- File duplikat dipindahkan ke folder _DUPLICATE
- Judul hasil rename otomatis disimpan ke judul.txt
- judul.txt otomatis di-sort alfabet

---

## Struktur File

Pastikan file berikut berada dalam folder yang sama:

nekopoi-renamer.ps1  
author.txt  
keyword.txt  
judul.txt  

---

## author.txt

Daftar author / studio.  
Satu baris = satu author.

Contoh:

Horny Herring Studios  
CBX-CJW  
Peh-koi  
Misumi  
MAKODA  

---

## keyword.txt

Daftar keyword yang harus tetap kapital (tidak di-TitleCase).

Contoh:

TK  
UKS  
ZZZ  
HSR  
UNCENSORED  
FGO  

---

## judul.txt

Database judul yang sudah pernah diproses.
Digunakan untuk mencegah rename judul duplikat.

Contoh isi:

EBWH-063 - U 480P  
SONE-788 Nekpoi - U 480P  

---

## Contoh Rename

Sebelum:

[NekoPoi]_EBWH-063-U_[480p].mp4

Sesudah:

EBWH-063 - U 480P.mp4

---

Sebelum:

NekoPoi_720p_Horny_Herring_Studios_Lyriel_Elf_Maid_from_A_House.mp4

Sesudah:

Horny Herring Studios - Lyriel Elf Maid From A House 720P.mp4

---

## Perilaku Duplikat

Jika judul:
- sudah ada di judul.txt, atau
- muncul dua kali dalam satu proses

Maka file:
- tidak akan di-rename
- dipindahkan ke folder _DUPLICATE
- diberi peringatan di console

---

## Cara Pakai

1. Buka PowerShell di folder script
2. Jalankan:

cleanner.bat

Jika script tidak bisa dijalankan, aktifkan dulu:

Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

---

## Catatan

- Script hanya mengubah nama file, bukan isi video
- Aman untuk ribuan file
- Fokus ke konsistensi arsip jangka panjang

---

Gunakan dengan bijak.
Koleksi rapi, hidup lebih tenang.
