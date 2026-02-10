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
TITLE_REGISTRY = "judul.debug.txt"

DRY_RUN = True  # Ubah ke True kalau mau test tanpa rename/move, Ubah ke False kalau mau langsung rename/move

# ==============================
# LOAD FILES
# ==============================

author_list = []
if os.path.exists(AUTHOR_FILE):
    with open(AUTHOR_FILE, "r", encoding="utf-8") as f:
        author_list = [line.strip().lower() for line in f if line.strip()]

keyword_list = []
if os.path.exists(KEYWORD_FILE):
    with open(KEYWORD_FILE, "r", encoding="utf-8") as f:
        keyword_list = [line.strip() for line in f if line.strip()]

seen_titles = set()
if os.path.exists(TITLE_REGISTRY):
    with open(TITLE_REGISTRY, "r", encoding="utf-8") as f:
        for line in f:
            seen_titles.add(line.strip().lower())

# ==============================
# CLEANING FUNCTIONS
# ==============================

def clean_symbols(name):
    name = re.sub(r'[\[\]{}()]', ' ', name)
    name = re.sub(r'[_]+', ' ', name)
    name = re.sub(r'\s{2,}', ' ', name)
    return name.strip(" -").strip()

def remove_domains(name):
    name = re.sub(r'https?://\S+', '', name, flags=re.I)
    name = re.sub(r'www\.\S+', '', name, flags=re.I)
    name = re.sub(r'\b[a-z0-9-]+\.(care|fun|tv|id|io|xyz|site|club|live|win|net|org|cc|me|pw|biz|info|asia|us|uk|pro|lol|trade|host|band|top|cam|red|pink|sexy|ninja|download|stream|watch|video|porn|sex|adult|cyou)\b', '', name, flags=re.I)
    return name

def extract_resolution(name):
    m = re.search(r'\b(360|480|720|1080|1440|2160)p?\b', name, re.I)
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

            # Normalize
            code_extract = raw.upper()
            code_extract = re.sub(r'\s+', '', code_extract)
            code_extract = code_extract.replace('_', '-')

            # ===== FC2 SPECIAL HANDLING =====
            fc2_ppv = re.search(r'FC2[-_\s]*PPV[-_\s]*(\d+)', raw, re.I)
            fc2_plain = re.search(r'FC2[-_\s]*(\d+)', raw, re.I)

            if fc2_ppv:
                code = f"FC2-PPV-{fc2_ppv.group(1)}"
            elif fc2_plain:
                code = f"FC2-PPV-{fc2_plain.group(1)}"
            else:
                code = code_extract

            # Rapihin dash
            code = re.sub(r'-+', '-', code).strip('-')

            return code

    return ""


def extract_studio(name):
    lowered = name.lower()
    for author in author_list:
        if author in lowered:
            return author.title()
    return ""

def enforce_keywords(name):
    for keyword in keyword_list:
        pattern = re.compile(re.escape(keyword), re.I)
        name = pattern.sub(keyword, name)
    return name

# ==============================
# BUILD NAME
# ==============================

def build_name(filename):
    name, ext = os.path.splitext(filename)

    name = remove_domains(name)
    name = clean_symbols(name)

    code = extract_code(name)
    studio = extract_studio(name)
    reso = extract_resolution(name)
    uncen = extract_uncen(name)

    if code:
        escaped = re.escape(code)
        flexible = escaped.replace(r'\-', r'[-_\s]*')
        name = re.sub(r'(?i)\b' + flexible + r'\b', '', name)

    if studio:
        name = re.sub(re.escape(studio), '', name, flags=re.I)

    name = re.sub(r'\b(360|480|720|1080|1440|2160)p?\b', '', name, flags=re.I)
    name = re.sub(r'\b(U|UC|UNCEN|UNCENSORED)\b', '', name, flags=re.I)

    name = clean_symbols(name)
    name = enforce_keywords(name)
    name = clean_symbols(name)

    parts = []

    if code:
        parts.append(code)

    if studio and studio.lower() not in name.lower():
        parts.append(studio)

    if name:
        parts.append(name)

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

# ==============================
# MAIN LOOP
# ==============================

for file in os.listdir(BASE_DIR):
    if not any(file.lower().endswith(ext) for ext in VIDEO_EXT):
        continue

    old_path = os.path.join(BASE_DIR, file)
    new_name, code = build_name(file)
    new_path = os.path.join(BASE_DIR, new_name)

    title_key = new_name.lower().strip()

    # === TITLE NULL CHECK ===
    name_only = os.path.splitext(new_name)[0].strip()
    if not name_only:
        print(f"[TITLE NULL] {file}")
        title_null_count += 1
        continue

    is_duplicate = title_key in seen_titles

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
            shutil.move(new_path, destination)

    elif code:
        destination = os.path.join(real_folder, new_name)
        print(f"[MOVED] {new_name} -> Real/")
        real_count += 1
        if not DRY_RUN:
            shutil.move(new_path, destination)

    else:
        lower = file.lower()
        if "snapsave" in lower or "fbdownload" in lower:
            destination = os.path.join(lainnya_folder, new_name)
            print(f"[MOVED] {new_name} -> Lainnya/")
            lainnya_count += 1
            if not DRY_RUN:
                shutil.move(new_path, destination)
        else:
            lainnya_count += 1

    seen_titles.add(title_key)


# ==============================
# SAVE REGISTRY
# ==============================

if not DRY_RUN:
    with open(TITLE_REGISTRY, "w", encoding="utf-8") as f:
        for title in sorted(seen_titles):
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
print("=================================")
