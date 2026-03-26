import os
import re
import shutil

# ==============================
# CONFIG
# ==============================

# Sesuaikan ekstensi video yang mau diproses, bisa ditambahin atau dikurangin sesuai kebutuhan. Pastikan semua ekstensi dalam bentuk lowercase untuk memudahkan pengecekan.
VIDEO_EXT = [".mp4", ".mkv", ".mov", ".webm"]
BASE_DIR = os.getcwd()
AUTHOR_FILE = "author.txt"
KEYWORD_FILE = "keyword.txt"
TITLE_REGISTRY = "judul.txt"

DRY_RUN = False  # Ubah ke True kalau mau test tanpa rename/move, Ubah ke False kalau mau langsung rename/move

# Daftar keyword NTR yang akan dideteksi di filename, termasuk variasi dan sinonimnya, supaya bisa langsung ditangkap sebagai indikasi NTR dan ditambahkan prefix "NTR" di title. Ini akan membantu memastikan kalau ada file dengan tema NTR, bisa langsung dikenali dan diproses dengan benar.
NTR_KEYWORDS = [
    "ntr", "netorare", "netori", "netorase", "cheating", "cuckold", "cuck", "affair", "cuckolded", "cucked", "cuckolding", "cuckoldry", "adultery", "infidelity", "betrayal", "unfaithful", "side piece", "stolen wife", "wife sharing", "partner sharing", "stolen", "sharing", "shared", "nettori", "nettorare", "nettorase"
]

# Fungsi untuk memindahkan file dengan aman, memastikan kalau ada file dengan nama yang sama di tujuan, file yang dipindahkan gak akan menimpa file yang sudah ada, tapi akan diberi suffix angka untuk membedakan. Ini akan membantu mencegah kehilangan data akibat penimpaan file, terutama kalau ada kasus duplikat yang gak terdeteksi sebelumnya.
def safe_move(src, dst):
    if os.path.exists(dst):
        base, ext = os.path.splitext(dst)
        counter = 1
        while os.path.exists(f"{base}_{counter}{ext}"):
            counter += 1
        dst = f"{base}_{counter}{ext}"
    shutil.move(src, dst)
    
# ==============================
# LOAD FILES
# ==============================

# Load author list dan buat map untuk case-sensitive matching, supaya bisa deteksi nama studio dengan lebih akurat berdasarkan daftar di author.txt, tapi tetap mempertahankan case aslinya untuk ditampilkan di title. Juga termasuk handling untuk memastikan kalau ada nama studio baru yang valid ditemukan di filename, bisa langsung di-auto-add ke author.txt tanpa harus restart script.
author_list = []
author_map = {}

# Load author list dari author.txt, simpan dalam bentuk lowercase di author_list untuk matching yang case-insensitive, dan simpan mapping ke case asli di author_map supaya bisa ditampilkan dengan benar di title nanti. Ini akan membantu memastikan nama studio yang terdeteksi dari filename bisa dicocokkan dengan daftar di author.txt dengan lebih akurat, tanpa khawatir soal perbedaan kapitalisasi.
if os.path.exists(AUTHOR_FILE):
    with open(AUTHOR_FILE, "r", encoding="utf-8") as f:
        for line in f:
            clean = line.strip()
            if clean:
                author_list.append(clean.lower())
                author_map[clean.lower()] = clean

# Load keyword list untuk enforce keywords, supaya bisa memastikan keyword tertentu selalu dalam format yang konsisten di title, misal "Live2D" selalu jadi "LIVE2D", "NTR" selalu jadi "NTR", dll, tanpa mempedulikan bagaimana aslinya di filename. Ini akan membantu menjaga konsistensi penamaan di seluruh koleksi.
keyword_list = []
if os.path.exists(KEYWORD_FILE):
    with open(KEYWORD_FILE, "r", encoding="utf-8") as f:
        keyword_list = [line.strip() for line in f if line.strip()]

# Load existing titles dari judul.txt untuk deteksi duplikat, simpan dalam bentuk lowercase di seen_titles_lower untuk matching yang case-insensitive, dan simpan juga dalam bentuk aslinya di existing_titles untuk nanti disimpan kembali ke judul.txt dengan format yang rapi. Ini akan membantu memastikan kalau ada title baru yang sudah pernah muncul sebelumnya, bisa langsung dideteksi sebagai duplikat tanpa khawatir soal perbedaan kapitalisasi atau format penulisan.
seen_titles_lower = set()
existing_titles = []

if os.path.exists(TITLE_REGISTRY):
    with open(TITLE_REGISTRY, "r", encoding="utf-8") as f:
        for line in f:
            clean_line = line.strip()
            if clean_line:
                existing_titles.append(clean_line)
                seen_titles_lower.add(clean_line.lower())

# ==============================
# CLEANING FUNCTIONS
# ==============================

# Fungsi untuk membersihkan simbol-simbol yang tidak diinginkan dari nama file, seperti tanda kurung, underscore, titik, dan mengganti multiple spasi dengan single space. Juga termasuk handling khusus untuk tanda hubung yang sering muncul di filename, supaya gak jadi noise di title. Fungsi ini akan memastikan nama yang dihasilkan lebih bersih dan rapi sebelum diproses lebih lanjut.
def clean_symbols(name):
    name = re.sub(r'[\[\]{}()]', ' ', name)
    name = re.sub(r'[_]+', ' ', name)
    name = re.sub(r'\s{2,}', ' ', name)
    name = re.sub(r'\s*\.\s*', ' ', name)
    name = re.sub(r'-{2,}.*$', '', name)
    return name.strip(" -").strip()

# Fungsi untuk menghapus domain, URL, dan variasi "nekopoi" dari nama file, supaya gak muncul di title. Ini termasuk deteksi berbagai macam TLD yang umum dipakai di situs-situs semacam ini, serta handling khusus untuk variasi "nekopoi" yang sering muncul dengan spasi atau simbol di antaranya.
def remove_domains(name):
    name = re.sub(r'https?://\S+', '', name, flags=re.I)
    name = re.sub(r'www\.\S+', '', name, flags=re.I)
    name = re.sub(r'(?i)nekopoi[-_]?care', '', name)
    name = re.sub(r'(?i)\bcare\b', '', name)
    name = re.sub(r'\b[a-z0-9-]+\.(care|fun|tv|id|io|xyz|site|club|live|win|net|org|cc|me|pw|biz|info|asia|us|uk|pro|lol|trade|host|band|top|cam|red|pink|sexy|ninja|download|stream|watch|video|porn|sex|adult|cyou)\b', '', name, flags=re.I)
    return name

# Fungsi untuk mengekstrak resolusi dengan berbagai variasi format yang mungkin muncul di filename, dan memastikan hasilnya selalu dalam format standar (misal "1080P" atau "720P") kalau terdeteksi, atau "" kalau tidak terdeteksi.
def extract_resolution(name):
    m = re.search(r'(360|480|720|1080|1440|2160)p?\b', name, re.I)
    return m.group(0).upper() if m else ""

# Fungsi untuk mengekstrak status uncensored, dengan berbagai variasi keyword yang mungkin muncul di filename, dan memastikan hasilnya selalu "UNCENSORED" kalau terdeteksi, atau "" kalau tidak terdeteksi.
def extract_uncen(name):
    if re.search(r'\b(U|UC|UNCEN|UNCENSORED)\b', name, re.I):
        return "UNCENSORED"
    return ""

# Fungsi untuk mengekstrak kode dengan berbagai pola, termasuk deteksi aman untuk menghindari ketuker antara prefix dan number, serta handling khusus untuk FC2 yang punya format unik. Fungsi ini juga sudah termasuk safety fix untuk kasus kebalik prefix-number, dan memastikan hasilnya selalu dalam format PREFIX-NUMBER, serta menghapus kode dari nama utama supaya gak muncul lagi di title.
def extract_code(name):
    name = re.sub(r'#\s*[A-Z0-9]+', '', name)
    name = re.sub(r'#', '', name)
    patterns = [
        r'(?i)FC2[-_\s]*PPV[-_\s]*(\d{3,9})',
        r'(?i)FC2[-_\s]*(\d{3,9})',
        r'(?i)(KBJ)[-_\s]?(\d{6,12})',
        r'(?i)(CN)[-_\s]?(\d{6,12})',
        r'(?i)(CUS)[-_\s]?(\d{3,4})(-\d+)?',
        r'(?i)(MD)[-_\s]?(\d{3,6})(-\d+)?',
        r'(?i)\b(SSNI|SSIS|DLDSS|MIAA|MIDV|IPX|STARS|CAWD|HMN|FSDSS|JUQ|FOCS|RCTD|REAL|KBJ|CN|MD|HEYZO|SIRO|1PON|CARIB|FPRE|CUS|JDKR|MDWP|PMA|MIAB|MIDA|MIMK|SNOS|START|MUDR|ABF|ABP|ADN|ATID|BF|BLK|EBOD|EBWH|GANA|GOPJ|JUR|MEYD|NIMA|NSFS|PRED|S-Cute|SUPA|TEK|WANZ|XVSR|546EROFV|JD|MT|420STH|COSH|420HHL|BOBB|DVRT|EYAN|29ID)[-_\s]*(\d{3,12})(?:[-_\s]*(U|UC|UNCEN|LEAK))?(\b|$)',
        r'(?i)\b([A-Z0-9]{3,5})[-_\s]*(\d{3,12})(?:[-_\s]*(U|UC|UNCEN|LEAK))?(\b|$)',
        r'(?i)\b([A-Z]{3,5})[-_\s]*(\d{3,6})(?:[-_\s]*\d)?(?:[-_\s]*(U|UC|UNCEN|LEAK))?(\b|$)'
    ]

    # Coba semua pattern satu per satu, kalau match, langsung proses untuk memastikan formatnya benar, dan return hasilnya. Kalau gak ada yang match, return "".
    for pat in patterns:
        match = re.search(pat, name)
        if match:
            # kalau pattern punya prefix + number
            if match.lastindex and match.lastindex >= 2:
                g1 = match.group(1)
                g2 = match.group(2)

                prefix = ""
                number = ""

                # DETEKSI AMAN (anti ketuker)
                if g1 and g2:
                    if re.match(r'^[A-Z0-9]+$', g1) and g2.isdigit():
                        prefix, number = g1.upper(), g2
                    elif re.match(r'^[A-Z0-9]+$', g2) and g1.isdigit():
                        prefix, number = g2.upper(), g1
                    else:
                        # skip kalau ambiguous
                        continue

                suffix = match.group(3) if match.lastindex >= 3 else None

                code = f"{prefix}-{number}"
                if suffix:
                    code += f"-{suffix.upper()}"

                # 🔥 SAFETY FIX (anti kebalik 2.0)
                m_fix = re.match(r'^(\d+)-([A-Z0-9]+)$', code)
                if m_fix:
                    code = f"{m_fix.group(2)}-{m_fix.group(1)}"

                return code

            raw = match.group(0)

            raw = raw.upper()
            raw = re.sub(r'\s+', '', raw)
            raw = raw.replace('_', '-')

            # ===== FC2 HANDLING =====
            fc2_ppv = re.search(r'FC2[-_\s]*PPV[-_\s]*(\d+)', raw, re.I)
            fc2_plain = re.search(r'FC2[-_\s]*(\d+)', raw, re.I)

            if fc2_ppv:
                return f"FC2-PPV-{fc2_ppv.group(1)}"
            if fc2_plain:
                return f"FC2-PPV-{fc2_plain.group(1)}"

            # ===== NORMAL PREFIX-NUMBER FIX =====
            m = re.match(r'^([A-Z]+)(\d+)$', raw)
            if m:
                return f"{m.group(1)}-{m.group(2)}"

            # kalau sudah ada dash
            raw = re.sub(r'-+', '-', raw).strip('-')
            return raw

    return ""

# Fungsi untuk mengekstrak nama studio dengan prioritas dari author.txt dulu, baru dari pola "by XXX" di filename. Juga termasuk auto-add ke author.txt kalau nemu studio baru yang valid.
def extract_studio(name):
    # Prioritas 1: dari author list
    for author_lower in author_list:
        pattern = re.compile(rf'\b{re.escape(author_lower)}\b', re.I)
        if pattern.search(name):
            return author_map[author_lower]
        
    # Prioritas 2: by XXX
    by_match = re.search(
        r'(?i)\bby\s+([A-Za-z0-9][A-Za-z0-9\s&\'\-\.\(\)]+?)(?=\s+(?:\d{3,4}p?|U|UC|UNCEN|UNCENSORED|2D|3D|LIVE2D)\b|[\[\]\(\)]|$)',
        name
    )
    
    # Kalau ketemu pola "by XXX", lakukan cleanup dan validasi tambahan untuk memastikan ini benar-benar nama studio yang layak, bukan kata umum atau noise. Kalau valid, cek juga apakah sudah ada di author.txt, kalau belum, langsung auto-add ke author.txt supaya nanti bisa dikenali sebagai studio yang valid di file-file berikutnya tanpa harus restart script.
    if by_match:
        by_studio = by_match.group(1).strip()

        # cleanup
        by_studio = re.sub(r'[\s_]+$', '', by_studio)
        by_studio = re.sub(r'\s{2,}', ' ', by_studio)
        by_studio = by_studio.strip(" -_()")

        # filter
        BAD_WORDS = ["the", "a", "my", "your", "this", "that", "with", "from", "video", "uncensored", "episode"]

        # Validasi tambahan untuk memastikan ini benar-benar nama studio yang layak, bukan kata umum atau noise
        if (
            len(by_studio) >= 2 and
            not any(re.search(rf'\b{re.escape(b)}\b', by_studio, re.I) for b in BAD_WORDS) and
            not by_studio.lower().startswith(("http", "www", "by ")) and
            not re.search(r'\d{3,4}p', by_studio, re.I)
        ):
            by_studio_lower = by_studio.lower()

            # Auto-add ke author.txt kalau belum ada di list, supaya nanti bisa dikenali sebagai studio yang valid di file-file berikutnya tanpa harus restart script. Ini akan membantu memperkaya database author.txt secara otomatis berdasarkan temuan di filename, tanpa harus repot-repot edit manual setiap kali nemu studio baru yang valid.
            if by_studio_lower not in author_list:
                print(f"[AUTO-ADD AUTHOR] {by_studio} → tidak ada di author.txt → ditambahkan!")

                if not DRY_RUN:
                    print(f"   ↳ ditambahkan ke author.txt")
                    with open(AUTHOR_FILE, "a", encoding="utf-8") as f:
                        f.write(by_studio + "\n")
                else:
                    print(f"   ↳ (DRY RUN) tidak ditulis ke file")

                # Update list dan map di runtime juga supaya langsung bisa dipakai untuk file berikutnya tanpa harus reload
                author_list.append(by_studio_lower)
                author_map[by_studio_lower] = by_studio

            return by_studio

    return ""

# Fungsi untuk memastikan keyword tertentu selalu dalam format yang konsisten, misal "Live2D" selalu jadi "LIVE2D", "NTR" selalu jadi "NTR", dll, tanpa mempedulikan bagaimana aslinya di filename
def enforce_keywords(name):
    for keyword in keyword_list:
        pattern = re.compile(rf'\b{re.escape(keyword)}\b', re.I)
        name = pattern.sub(keyword, name)
    return name

# Fungsi untuk title case yang lebih pintar, mempertahankan uppercase kalau memang sudah uppercase (misal kode atau akronim), dan tetap kapitalisasi normal untuk kata biasa
def smart_title_case(text):
    def fix_word(w):
        # pisahkan simbol di depan kata (misal ~shadow)
        m = re.match(r'^([^A-Za-z0-9]*)(.*)$', w)
        if not m:
            return w

        prefix = m.group(1)
        core = m.group(2)

        if not core:
            return w

        if core.isupper():
            return prefix + core
        if any(c.isdigit() for c in core):
            return prefix + core

        return prefix + core.capitalize()

    return " ".join(fix_word(w) for w in text.split())

# Fungsi untuk mengekstrak dimension (Live2D, 2D, 3D) dari nama file, dengan berbagai variasi penulisan yang mungkin muncul, dan memastikan hasilnya selalu dalam format standar (misal "LIVE2D", "2D", "3D") kalau terdeteksi, atau "" kalau tidak terdeteksi.
def extract_dimension(name):
    m = re.search(r'(?i)\b(LIVE2D|L2D|2D|3D)\b', name)
    return m.group(0).upper() if m else ""

# ==============================
# BUILD NAME
# ==============================

def build_name(filename):
    name, ext = os.path.splitext(filename)
    original_name = name # simpan original untuk deteksi NTR

    # Deteksi NTR Dari Original Filename
    has_ntr = any(
        re.search(rf'(^|[\s_\-]){re.escape(keyword_ntr)}($|[\s_\-])', original_name.lower())
        for keyword_ntr in NTR_KEYWORDS
    )

    # Hapus domain, simbol, dan variasi "nekopoi"
    name = remove_domains(name)
    name = re.sub(r'(?i)ne\s*k\s*o\s*poi', '', name)
    name = clean_symbols(name)
    
    # slug detection (kalau dash terlalu banyak → kemungkinan dari URL)
    if name.count("-") >= 3:
        name = name.replace("-", " ")

    # Extract code, studio, resolution, uncensored, dimension dulu supaya bisa dihapus dari name sebelum proses selanjutnya
    code = extract_code(name)
    studio = extract_studio(name)
    reso = extract_resolution(name)
    uncen = extract_uncen(name)
    dim = extract_dimension(name)

    # Hapus kode dari nama utama supaya gak muncul lagi di title, tapi tetap simpan di variable code untuk nanti dijadikan prefix
    if code:
        # hapus semua variasi kode fleksibel
        flexible = code.replace('-', r'[-_\s]*')
        name = re.sub(rf'(?i)\b{flexible}\b', '', name)

    # khusus FC2 → hapus angka mentahnya juga
    if code and code.startswith("FC2-PPV-"):
        number = code.split("-")[-1]
        name = re.sub(rf'(?i)\b{number}\b', '', name)

    # Hapus nama studio dari nama utama supaya gak muncul lagi di title, tapi tetap simpan di variable studio untuk nanti dijadikan prefix
    if studio:
        name = re.sub(re.escape(studio), '', name, flags=re.I)
        name = re.sub(r'(?i)\bby\s*', '', name)  # hapus "By ", "by ", "BY " dll
        name = name.strip()

    # Hapus resolusi dan uncensored dari nama utama supaya gak muncul lagi di title, tapi tetap simpan di variable reso dan uncen untuk nanti dijadikan suffix
    name = re.sub(
        r'(\d+)?(360|480|720|1080|1440|2160)p?\b',
        lambda m: m.group(1) if m.group(1) else '',
        name,
        flags=re.I
    )
    name = re.sub(r'\b(U|UC|UNCEN|UNCENSORED)\b', '', name, flags=re.I)
    
    # Hapus dimension dari nama utama supaya gak muncul lagi di title, tapi tetap simpan di variable dim untuk nanti dijadikan prefix
    if dim:
        name = re.sub(rf'\b{re.escape(dim)}\b', '', name, flags=re.I)

    name = clean_symbols(name)
    name = name.replace("–", "-").replace("—", "-")
    
    # ===== Extract episode number di akhir =====
    episode = ""

    # Jangan tangkap angka kalau sebelumnya ada kata Season
    if not re.search(r'Season\s+\d{1,2}$', name, re.IGNORECASE):
        m_ep = re.search(r'(?<![A-Za-z0-9])(\d{1,2})$', name)
        if m_ep:
            episode = m_ep.group(1).zfill(2)
            name = re.sub(r'(?:-|_)?\s*\d{1,2}$', '', name).strip()

    # hapus simbol gantung di akhir
    name = re.sub(r'[-\s]+$', '', name).strip()
    name = re.sub(r'\s-\s-', ' - ', name)

    parts = []  
    
    # NTR Prefix
    if has_ntr:
        parts.append("NTR")

    # Code Prefix
    if code:
        parts.append(code)

    # Studio Prefix
    if studio and studio.lower() not in name.lower():
        parts.append(studio)

    # Title + Dimension Prefix
    if name:
        name = smart_title_case(name)
        name = enforce_keywords(name)
        if dim:
            name = f"{dim} {name}"
        parts.append(name)
        
    # Episode Prefix (karena biasanya di akhir, jadi dipasang paling belakang)
    if episode:
        parts.append(episode)

    # Gabungkan semua bagian dengan " - "
    final = " - ".join(parts).strip()

    # Tambahkan resolusi dan uncensored di akhir
    suffix = []
    if uncen:
        suffix.append(uncen)
    if reso:
        suffix.append(reso)

    # Kalau ada suffix, tambahkan dengan spasi
    if suffix:
        final = f"{final} {' '.join(suffix)}"

    # Bersihkan spasi ganda yang mungkin muncul
    final = re.sub(r'\s{2,}', ' ', final).strip()

    # Tambahkan ekstensi kembali
    return final + ext, code

# ==============================
# FOLDER SETUP
# ==============================

real_folder = os.path.join(BASE_DIR, "Real")
dup_folder = os.path.join(BASE_DIR, "_DUPLICATE")
lainnya_folder = os.path.join(BASE_DIR, "Lainnya")

for folder in [real_folder, dup_folder, lainnya_folder]:
    os.makedirs(folder, exist_ok=True)

# ==============================
# STATS
# ==============================

renamed_count = 0
skip_clean_count = 0
title_null_count = 0
real_count = 0
lainnya_count = 0
duplicate_move_count = 0
tetap_count = 0
    
# ==============================
# MAIN LOOP
# ==============================

for file in os.listdir(BASE_DIR):
    if not any(file.lower().endswith(ext) for ext in VIDEO_EXT):
        continue

    lower = file.lower()
    old_path = os.path.join(BASE_DIR, file)

    is_downloader = any(x in lower for x in [
        "snapsave",
        "fbdownload",
        "fdownloader",
        "savefrom",
        "fbcdn",
        "ssstik",
        "facebook"
    ])

    clean = re.sub(r'[\s_\-\.]', '', lower)
    is_nekopoi = any(x in clean for x in ["nekopoi", "nekpoi"])
    
    has_hashtag = "#" in file
    
    # PRE-CHECK CODE / RESOLUSI DULU
    temp_name = remove_domains(os.path.splitext(file)[0])
    temp_name = clean_symbols(temp_name)
    temp_code = extract_code(temp_name)
    temp_reso = extract_resolution(temp_name)
    temp_conf = temp_reso or temp_code
    
    # ==============================
    # HARD BYPASS HASHTAG
    # ==============================
    if has_hashtag:
        destination = os.path.join(lainnya_folder, file)
        print(f"[HASHTAG BYPASS] {file} -> Lainnya/")
        lainnya_count += 1

        if not DRY_RUN:
            safe_move(old_path, destination)
        continue

    # ==============================
    # HARD BYPASS DOWNLOADER
    # ==============================
    if is_downloader:
        destination = os.path.join(lainnya_folder, file)
        print(f"[DOWNLOADER] {file} -> Lainnya/")
        lainnya_count += 1

        if not DRY_RUN:
            safe_move(old_path, destination)
        continue

    # ==============================
    # HARD BYPASS NON NEKOPOI
    # ==============================
    if not temp_conf and not is_nekopoi:
        destination = os.path.join(lainnya_folder, file)
        print(f"[MOVED NON-NEKOPOI] {file} -> Lainnya/")
        lainnya_count += 1

        if not DRY_RUN:
            safe_move(old_path, destination)
        continue

    # ==============================
    # NORMAL FLOW
    # ==============================
    new_name, code = build_name(file)
    new_path = os.path.join(BASE_DIR, new_name)

    title_without_ext = os.path.splitext(new_name)[0].strip()
    title_key = title_without_ext
    title_key_lower = title_key.lower()

    name_only = os.path.splitext(new_name)[0].strip()
    if not name_only:
        print(f"[TITLE NULL] {file}")
        title_null_count += 1
        continue

    is_duplicate = title_key_lower in seen_titles_lower

    # === RENAME ===
    if new_name != file:
        print(f"[RENAMED] {file}  ->  {new_name}")
        renamed_count += 1
        if not DRY_RUN:
            os.rename(old_path, new_path)
    else:
        new_path = old_path
        skip_clean_count += 1

    # === MOVE LOGIC ===
    if is_duplicate:
        destination = os.path.join(dup_folder, new_name)
        print(f"[DUPLICATE] {new_name} -> _DUPLICATE/")
        duplicate_move_count += 1
        if not DRY_RUN:
            safe_move(new_path, destination)

    elif code:
        destination = os.path.join(real_folder, new_name)
        print(f"[MOVED] {new_name} -> Real/")
        real_count += 1
        if not DRY_RUN:
            safe_move(new_path, destination)

    else:
        tetap_count += 1

    if title_key_lower not in seen_titles_lower:
        existing_titles.append(title_key)
        seen_titles_lower.add(title_key_lower)

# ==============================
# SAVE REGISTRY
# ==============================

if not DRY_RUN:
    sorted_titles = sorted(existing_titles, key=lambda x: x.lower())

    with open(TITLE_REGISTRY, "w", encoding="utf-8") as f:
        for title in sorted_titles:
            f.write(title + "\n")

# ==============================
# SUMMARY
# ==============================

print("\n=========== RINGKASAN ===========")
print(f"✔ Di-rename    : {renamed_count}")
print(f"⇰ Sudah rapi   : {skip_clean_count}")
print(f"↻ Judul kosong : {title_null_count}")
print("=================================")

print("\n===========  OUTPUT  ===========")
print(f"✔ Real         : {real_count}")
print(f"⇰ Lainnya      : {lainnya_count}")
print(f"⇲ Duplicate    : {duplicate_move_count}")
print(f"• Tetap        : {tetap_count}")
print("=================================")
