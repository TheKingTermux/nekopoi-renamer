import os
import re
import shutil

# ==============================
# CONFIG
# ==============================

VIDEO_EXT = [".mp4", ".mkv", ".mov", ".webm"]
BASE_DIR = os.getcwd()
AUTHOR_FILE = "author.txt"
KEYWORD_FILE = "keyword.txt"
TITLE_REGISTRY = "judul.txt"

DRY_RUN = False  # Ubah ke True kalau mau test tanpa rename/move, Ubah ke False kalau mau langsung rename/move

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

author_list = []
author_map = {}

if os.path.exists(AUTHOR_FILE):
    with open(AUTHOR_FILE, "r", encoding="utf-8") as f:
        for line in f:
            clean = line.strip()
            if clean:
                author_list.append(clean.lower())
                author_map[clean.lower()] = clean

keyword_list = []
if os.path.exists(KEYWORD_FILE):
    with open(KEYWORD_FILE, "r", encoding="utf-8") as f:
        keyword_list = [line.strip() for line in f if line.strip()]

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

def clean_symbols(name):
    name = re.sub(r'[\[\]{}()]', ' ', name)
    name = re.sub(r'[_]+', ' ', name)
    name = re.sub(r'\s{2,}', ' ', name)
    name = re.sub(r'\s*\.\s*', ' ', name)
    name = re.sub(r'-{2,}.*$', '', name)
    return name.strip(" -").strip()

def remove_domains(name):
    name = re.sub(r'https?://\S+', '', name, flags=re.I)
    name = re.sub(r'www\.\S+', '', name, flags=re.I)
    name = re.sub(r'(?i)nekopoi[-_]?care', '', name)
    name = re.sub(r'(?i)\bcare\b', '', name)
    name = re.sub(r'\b[a-z0-9-]+\.(care|fun|tv|id|io|xyz|site|club|live|win|net|org|cc|me|pw|biz|info|asia|us|uk|pro|lol|trade|host|band|top|cam|red|pink|sexy|ninja|download|stream|watch|video|porn|sex|adult|cyou)\b', '', name, flags=re.I)
    return name

def extract_resolution(name):
    m = re.search(r'(360|480|720|1080|1440|2160)p?\b', name, re.I)
    return m.group(0).upper() if m else ""

def extract_uncen(name):
    if re.search(r'\b(U|UC|UNCEN|UNCENSORED)\b', name, re.I):
        return "UNCEN"
    return ""

def extract_code(name):
    patterns = [
        r'(?i)FC2[-_\s]*PPV[-_\s]*(\d{3,9})',
        r'(?i)FC2[-_\s]*(\d{3,9})',
        r'(?i)(KBJ)[-_\s]?(\d{6,12})',
        r'(?i)(CN)[-_\s]?(\d{6,12})',
        r'(?i)(CUS)[-_\s]?(\d{3,4})(-\d+)?',
        r'(?i)(MD)[-_\s]?(\d{3,6})(-\d+)?',
        r'(?i)\b(SSNI|SSIS|DLDSS|MIAA|MIDV|IPX|STARS|CAWD|HMN|FSDSS|JUQ|FOCS|RCTD|REAL|KBJ|CN|MD|HEYZO|SIRO|1PON|CARIB|FPRE|CUS|JDKR|MDWP|PMA|MIAB|MIDA|MIMK|SNOS|START|MUDR|ABF|ABP|ADN|ATID|BF|BLK|EBOD|EBWH|GANA|GOPJ|JUR|MEYD|NIMA|NSFS|PRED|S-Cute|SUPA|TEK|WANZ|XVSR)[-_\s]*(\d{3,12})(?:[-_\s]*(U|UC|UNCEN|LEAK))?(\b|$)',
        r'(?i)\b([A-Z0-9]{3,5})[-_\s]*(\d{3,12})(?:[-_\s]*(U|UC|UNCEN|LEAK))?(\b|$)',
        r'(?i)\b([A-Z]{3,5})[-_\s]*(\d{3,6})(?:[-_\s]*\d)?(?:[-_\s]*(U|UC|UNCEN|LEAK))?(\b|$)'
    ]

    for pat in patterns:
        match = re.search(pat, name)
        if match:
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


def extract_studio(name):
    lowered = name.lower()
    for author_lower in author_list:
        if author_lower in lowered:
            return author_map[author_lower]
    return ""

def enforce_keywords(name):
    for keyword in keyword_list:
        pattern = re.compile(rf'\b{re.escape(keyword)}\b', re.I)
        name = pattern.sub(keyword, name)
    return name

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

# ==============================
# BUILD NAME
# ==============================

def build_name(filename):
    name, ext = os.path.splitext(filename)

    name = remove_domains(name)
    name = re.sub(r'(?i)ne\s*k\s*o\s*poi', '', name)
    name = clean_symbols(name)
    
    # slug detection (kalau dash terlalu banyak → kemungkinan dari URL)
    if name.count("-") >= 3:
        name = name.replace("-", " ")

    code = extract_code(name)
    studio = extract_studio(name)
    reso = extract_resolution(name)
    uncen = extract_uncen(name)

    if code:
        # hapus semua variasi kode fleksibel
        flexible = code.replace('-', r'[-_\s]*')
        name = re.sub(rf'(?i)\b{flexible}\b', '', name)

    # khusus FC2 → hapus angka mentahnya juga
    if code and code.startswith("FC2-PPV-"):
        number = code.split("-")[-1]
        name = re.sub(rf'(?i)\b{number}\b', '', name)


    if studio:
        name = re.sub(re.escape(studio), '', name, flags=re.I)

    name = re.sub(
        r'(\d+)?(360|480|720|1080|1440|2160)p?\b',
        lambda m: m.group(1) if m.group(1) else '',
        name,
        flags=re.I
    )
    name = re.sub(r'\b(U|UC|UNCEN|UNCENSORED)\b', '', name, flags=re.I)

    name = clean_symbols(name)
    name = name.replace("–", "-").replace("—", "-")
    
    # ===== Extract episode number di akhir =====
    episode = ""

    # Jangan tangkap angka kalau sebelumnya ada kata Season
    if not re.search(r'Season\s+\d{1,2}$', name, re.IGNORECASE):
        m_ep = re.search(r'(?:-|_)?\s*(\d{1,2})$', name)
        if m_ep:
            episode = m_ep.group(1).zfill(2)
            name = re.sub(r'(?:-|_)?\s*\d{1,2}$', '', name).strip()

        
    # hapus simbol gantung di akhir
    name = re.sub(r'[-\s]+$', '', name).strip()
    name = re.sub(r'\s-\s-', ' - ', name)

    parts = []  

    if code:
        parts.append(code)

    if studio and studio.lower() not in name.lower():
        parts.append(studio)

    if name:
        name = smart_title_case(name)
        name = enforce_keywords(name)
        parts.append(name)
        
    if episode:
        parts.append(episode)

    final = " - ".join(parts).strip()

    suffix = []
    if uncen:
        suffix.append(uncen)
    if reso:
        suffix.append(reso)

    if suffix:
        final = f"{final} {' '.join(suffix)}"

    final = re.sub(r'\s{2,}', ' ', final).strip()

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
        "fbcdn"
    ])

    clean = re.sub(r'[\s_\-\.]', '', lower)
    is_nekopoi = any(x in clean for x in ["nekopoi", "nekpoi"])
    
    # PRE-CHECK CODE / RESOLUSI DULU
    temp_name = remove_domains(os.path.splitext(file)[0])
    temp_name = clean_symbols(temp_name)
    temp_code = extract_code(temp_name)
    temp_reso = extract_resolution(temp_name)
    temp_conf = temp_reso or temp_code

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
    if not is_nekopoi and not temp_conf:
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

    title_key = new_name.strip()
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
