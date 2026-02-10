import os
import re

# ==============================
# CONFIG
# ==============================

VIDEO_EXT = [".mp4", ".mkv", ".mov", ".webm"]
BASE_DIR = os.getcwd()
AUTHOR_FILE = "author.txt"
KEYWORD_FILE = "keyword.txt"

# ==============================
# LOAD WHITELIST AUTHOR
# ==============================

author_list = []
if os.path.exists(AUTHOR_FILE):
    with open(AUTHOR_FILE, "r", encoding="utf-8") as f:
        author_list = [line.strip().lower() for line in f if line.strip()]

# ==============================
# LOAD KEYWORD ENFORCE
# ==============================

keyword_list = []
if os.path.exists(KEYWORD_FILE):
    with open(KEYWORD_FILE, "r", encoding="utf-8") as f:
        keyword_list = [line.strip() for line in f if line.strip()]

# ==============================
# REMOVE DOMAIN
# ==============================

def remove_domains(name):
    name = re.sub(r'https?://\S+', '', name, flags=re.I)
    name = re.sub(r'www\.\S+', '', name, flags=re.I)

    name = re.sub(
        r'\s?\.(care|fun|tv|id|io|xyz|site|club|live|win|net|org|cc|me|pw|biz|info|asia|us|uk|pro|lol|trade|host|band|top|cam|red|pink|sexy|ninja|download|stream|watch|video|porn|sex|adult|cyou)\b',
        '',
        name,
        flags=re.I
    )

    name = re.sub(
        r'\b[a-z0-9-]+\.(care|fun|tv|id|io|xyz|site|club|live|win|net|org|cc|me|pw|biz|info|asia|us|uk|pro|lol|trade|host|band|top|cam|red|pink|sexy|ninja|download|stream|watch|video|porn|sex|adult|cyou)\b',
        '',
        name,
        flags=re.I
    )

    return name

# ==============================
# CLEAN SYMBOL
# ==============================

def clean_symbols(name):
    name = re.sub(r'[\[\]{}()]', ' ', name)
    name = re.sub(r'[_]+', ' ', name)
    name = re.sub(r'\s{2,}', ' ', name)
    name = name.strip(" -")
    return name.strip()

# ==============================
# ENFORCE KEYWORD FORMAT
# ==============================

def enforce_keywords(name):
    for keyword in keyword_list:
        # cocokkan sebagai phrase utuh (bukan bagian kata)
        pattern = re.compile(r'(?<!\w)' + re.escape(keyword) + r'(?!\w)', re.I)
        name = pattern.sub(keyword, name)
    return name

# ==============================
# EXTRACT PARTS
# ==============================

def extract_resolution(name):
    match = re.search(r'\b(360|480|720|1080|1440|2160)p?\b', name, re.I)
    return match.group(0).upper() if match else ""

def extract_uncen(name):
    if re.search(r'(\b-U\b|\bUNCEN\b|\bUNCENSORED\b)', name, re.I):
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
        r'(?i)\b([A-Z0-9]{2,5})[-_\s]*(\d{3,12})(?:[-_\s]*(U|UC|UNCEN|LEAK))?(\b|$)',
        r'(?i)\b([A-Z]{3,5})[-_\s]*(\d{3,6})(?:[-_\s]*\d)?(?:[-_\s]*(U|UC|UNCEN|LEAK))?(\b|$)'
    ]

    for pat in patterns:
        match = re.search(pat, name)
        if match:
            raw = match.group(0)

            # Normalize
            code = raw.upper()
            code = re.sub(r'\s+', '', code)
            code = code.replace('_', '-')

            # FC2 special handling
            fc2_match = re.search(r'FC2[-_\s]*(?:PPV[-_\s]*)?(\d+)', raw, re.I)
            if fc2_match:
                code = f"FC2-PPV-{fc2_match.group(1)}"

            code = re.sub(r'-+', '-', code)
            code = code.strip('-')

            return code

    return ""

def extract_studio(name):
    match = re.search(r'By\s+(.+?)(?=\b\d{3,4}p\b|\b[A-Za-z]{2,6}-\d{2,6}\b|$)', name, re.I)
    if match:
        return clean_symbols(match.group(1)).title()

    lowered = name.lower()
    for author in author_list:
        if author in lowered:
            return author.title()

    return ""

# ==============================
# BUILD FINAL NAME
# ==============================

def build_name(filename):
    name, ext = os.path.splitext(filename)

    name = remove_domains(name)
    name = clean_symbols(name)

    code = extract_code(name)
    studio = extract_studio(name)
    reso = extract_resolution(name)
    uncen = extract_uncen(name)

    # ==========================
    # REMOVE EXTRACTED PARTS
    # ==========================

    if code:
        escaped = re.escape(code)
        flexible = escaped.replace(r'\-', r'[-_\s]*')
        pattern = re.compile(r'(?i)\b' + flexible + r'\b')
        name = pattern.sub('', name)

    if studio:
        name = re.sub(re.escape(studio), '', name, flags=re.I)

    name = re.sub(r'By\s+.+', '', name, flags=re.I)
    name = re.sub(r'\b(360|480|720|1080|1440|2160)p?\b', '', name, flags=re.I)
    name = re.sub(r'(\b-U\b|\bUNCEN\b|\bUNCENSORED\b)', '', name, flags=re.I)

    name = clean_symbols(name)

    # ==========================
    # ENFORCE KEYWORD
    # ==========================

    for keyword in keyword_list:
        pattern = re.compile(re.escape(keyword), re.I)
        name = pattern.sub(keyword, name)

    name = clean_symbols(name)

    # ==========================
    # BUILD STRUCTURE
    # ==========================

    parts = []

    if code:
        parts.append(code)

    if studio:
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
# BATCH RENAME
# ==============================

real_folder = os.path.join(BASE_DIR, "Real")
if not os.path.exists(real_folder):
    os.makedirs(real_folder)

for file in os.listdir(BASE_DIR):
    if any(file.lower().endswith(ext) for ext in VIDEO_EXT):

        old_path = os.path.join(BASE_DIR, file)

        new_name, code = build_name(file)
        new_path = os.path.join(BASE_DIR, new_name)

        # RENAME
        if new_name != file:
            print(f"[RENAMED] {file}  ->  {new_name}")
            os.rename(old_path, new_path)
        else:
            new_path = old_path

        # ==========================
        # MOVE KE FOLDER REAL
        # ==========================
        if code:
            destination = os.path.join(real_folder, new_name)

            if not os.path.exists(destination):
                print(f"[MOVED] {new_name} -> Real/")
                os.rename(new_path, destination)