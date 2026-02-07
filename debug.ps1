$videoExt = @(".mp4",".mkv",".mov",".webm")
$seenTitles = @{}
$renamedCount = 0
$skipCleanCount = 0
$duplicateMoveCount = 0
$titleNullCount = 0
$realCount = 0
$lainnyaCount = 0

# Folder pembuangan duplikat
$dupFolder = "_DUPLICATE"
if (-not (Test-Path $dupFolder)) { New-Item -ItemType Directory -Name $dupFolder | Out-Null }

# Folder baru untuk snapsave & non-nekopoi
$lainnyaFolder = "Lainnya"
if (-not (Test-Path $lainnyaFolder)) { New-Item -ItemType Directory -Name $lainnyaFolder | Out-Null }

# Load author whitelist
$authorFile = "author.txt"
$authorList = @()
if (Test-Path $authorFile) { $authorList = Get-Content $authorFile | Where-Object { $_.Trim() -ne "" } }

# Load keyword whitelist
$keywordFile = "keyword.txt"
$keywordList = @()
if (Test-Path $keywordFile) { $keywordList = Get-Content $keywordFile | Where-Object { $_.Trim() -ne "" } }

# Load title registry
$titleFile = "judul.txt"
$titleRegistry = @{}
if (Test-Path $titleFile) {
    Get-Content $titleFile | ForEach-Object {
        $k = ($_ -replace '\s+',' ').Trim().ToLower()
        if ($k) { $titleRegistry[$k] = $true }
    }
}

function Add-TitleRegistry {
    param ([string]$Title, [string]$File = "judul.txt")
    Add-Content -Path $File -Value "`r`n$Title" -Encoding UTF8
}

function Sort-TitleRegistry {
    param ([string]$File = "judul.txt")
    if (-not (Test-Path $File)) { return }
    $sorted = Get-Content $File | Where-Object { $_.Trim() -ne "" } | Sort-Object { $_.ToLower() } -Unique
    Set-Content -Path $File -Value $sorted -Encoding UTF8
}

Get-ChildItem -File | Where-Object { $videoExt -contains $_.Extension.ToLower() } | ForEach-Object {
    $original = $_.Name
    $name = $_.BaseName
    $ext = $_.Extension
    $currentDir = $_.DirectoryName

    $reso = ""
    $dim = ""
    $studio = ""
    $code = ""
    $hasAuthor = $false
    $isFallbackToCode = $false

    try {
        # 1. Ekstrak RESOLUTION dulu
        if ($name -match '(?i)(\d{3,4})[pP](?![^0-9]*\d{3,4}[pP])') {
            $reso = $Matches[1] + "P"
            $name = $name -replace [regex]::Escape($Matches[0]), ''
        }

        # 2. Ekstrak CODE JAV – pakai pola sederhana + post-process FC2-PPV
        $patterns = @(
            '(?i)FC2[-_\s]*PPV[-_\s]*(\d{3,9})',
            '(?i)FC2[-_\s]*(\d{3,9})',
            '(?i)(KBJ)[-_\s]?(\d{6,12})',
            '(?i)(CN)[-_\s]?(\d{6,12})',
            '(?i)(CUS)[-_\s]?(\d{3,4})(-\d+)?',
            '(?i)(MD)[-_\s]?(\d{3,6})(-\d+)?',
            '(?i)\b(SSNI|SSIS|DLDSS|MIAA|MIDV|IPX|STARS|CAWD|HMN|FSDSS|JUQ|FOCS|RCTD|REAL|KBJ|CN|MD|HEYZO|SIRO|1PON|CARIB|FPRE|CUS|JDKR|MDWP|PMA|MIAB|MIDA|MIMK|SNOS|START|MUDR|ABF|ABP|ADN|ATID|BF|BLK|EBOD|EBWH|GANA|GOPJ|JUR|MEYD|NIMA|NSFS|PRED|S-Cute|SUPA|TEK|WANZ|XVSR)[-_\s]*(\d{3,12})(?:[-_\s]*(U|UC|UNCEN|LEAK))?(\b|$)',
            '(?i)\b([A-Z0-9]{3,5})[-_\s]*(\d{3,12})(?:[-_\s]*(U|UC|UNCEN|LEAK))?(\b|$)',
            '(?i)\b([A-Z]{3,5})[-_\s]*(\d{3,6})(?:[-_\s]*\d)?(?:[-_\s]*(U|UC|UNCEN|LEAK))?(\b|$)'
        )

        foreach ($pat in $patterns) {
            if ($name -match $pat) {
                $codeExtract = $Matches[0].ToUpper() -replace '\s+', '' -replace '_', '-'
                # Khusus FC2-PPV selalu tambah prefix lengkap
                if ($codeExtract -match '^FC2PPV(\d+)$') {
                    $codeExtract = "FC2-PPV-" + $Matches[1]
                } elseif ($codeExtract -match '^FC2(\d+)$') {
                    $codeExtract = "FC2-PPV-" + $Matches[1]
                }
                $code = $codeExtract.ToUpper() -replace '-\s*', '-'  # hapus spasi setelah "-"
                $name = $name -replace [regex]::Escape($Matches[0]), ''
            }
        }

        # 3. Author By xxx
        if ($name -match '(?i)\bBy\s+([^\[\]\(\)\-]+)') {
            $studio = $Matches[1].Trim()
            $name = $name -replace '(?i)\bBy\s+[^\[\]\(\)\-]+',''
            $hasAuthor = $true
        }

        # 4. Author whitelist prefix – pakai nama asli dari txt
        if (-not $hasAuthor) {
            foreach ($a in $authorList) {
                $esc = [regex]::Escape($a)
                $escFlex = $esc -replace '\ ', '[\s_]+'
                if ($name -match "(?i)^\s*($escFlex)([\s_-]+)?") {
                    $studio = $a
                    $name = $name -replace "(?i)^\s*($escFlex)([\s_-]+)?", ''
                    $hasAuthor = $true
                    break
                }
            }
        }

        # 5. Hapus domain & nekopoi
        $name = $name -replace '(?i)nekopoi|neko poi|javhd|javlibrary|javmost|javfinder|javtiful|nekpoi|nek poi', ''
        $name = $name -replace '(?i)\.(care|fun|tv|id|io|xyz|site|club|live|win|net|org|cc|me|pw|biz|info|asia|us|uk|pro|lol|trade|host|band|top|cam|red|pink|sexy|ninja|download|stream|watch|video|porn|sex|adult|cyou)\b', ''

        # 6. Dimension
        if ($name -match '(?i)\b(LIVE2D|L2D|2D|3D)\b') {
            $dim = $Matches[0].ToUpper()
            $name = $name -replace '(?i)\b(LIVE2D|L2D|2D|3D)\b',''
        }

        # 7. Clean symbol
        $name = $name -replace '[\[\]{}()_]+',' '

        # 8. Normalize (gak pakai ToTitleCase biar kode & nama lebih konsisten)
        $name = ($name -replace '\s{2,}',' ').Trim()

        # --- DETEKSI & BERSIHKAN UNCENSORED DULU (sebelum fallback) ---
        $uncenTag = ""

        # Cek indikasi uncen dari nama asli ATAU suffix -U di kode
        if ($original -match '(?i)\b(uncen|uncensored|leak)\b' -or ($code -and $code -match '-U$')) {
            $uncenTag = "UNCENSORED"
        }

        # Hapus kata uncen dari judul supaya gak kebawa ke tengah
        # Pake \b biar cuma hapus kata utuh, gak nyentuh "uncertain" atau "luncur" dll
        $name = $name -replace '(?i)\b(uncen|uncensored|leak)\b',''
        $name = $name -replace '\s{2,}',' '
        $name = $name.Trim()

        # 9. Fallback aman – kalau kosong pakai code, tapi jangan tambah double di final
        $isFallbackToCode = $false
        if ([string]::IsNullOrWhiteSpace($name)) {
            if ($code) {
                $name = $code
                $isFallbackToCode = $true
                Write-Host "Judul kosong → pakai code: $code" -ForegroundColor Yellow
            } else {
                $name = ($_.BaseName -replace '(?i)nekopoi|uncen|uncensored|\.(care|fun|tv|id|io|xyz).*',' ' -replace '[\[\]{}()_]+',' ' -replace '\s{2,}',' ').Trim()
                if ([string]::IsNullOrWhiteSpace($name)) { $name = "Video_Tanpa_Judul" }
                Write-Host "Fallback clean basename: $name" -ForegroundColor DarkYellow
            }
            $titleNullCount++
        }

        # Cek ulang Author (tahap 2)
        if ($name -match '(?i)\bBy\s+([^\[\]\(\)\-]+)') {
            $studio = $Matches[1].Trim()
            $name = $name -replace '(?i)\bBy\s+[^\[\]\(\)\-]+',''
            $hasAuthor = $true
        }
        if (-not $hasAuthor) {
            foreach ($a in $authorList) {
                $esc = [regex]::Escape($a)
                $escFlex = $esc -replace '\ ', '[\s_]+'
                if ($name -match "(?i)^\s*($escFlex)([\s_-]+)?") {
                    $studio = $a
                    $name = $name -replace "(?i)^\s*($escFlex)([\s_-]+)?", ''
                    $hasAuthor = $true
                    break
                }
            }
        }

        # 10. Build final – kode upper case, UNCENSORED paling akhir sebelum resolusi
        $final = ""
        if ($code -and -not $isFallbackToCode) { $final += $code }
        if ($dim) { $final += $dim + " " }
        if ($studio) { $final += $studio + " - " }
        $final += " - " + $name  # pemisah " - " di sini, biar cuma muncul kalau perlu

        # Tambah NTR di paling depan kalau nama asli mengandung Netorare / NTR
        if ($original -match '(?i)\b(NTR|Netorare)\b') {
            $final = "NTR - " + $final
        }

        # Tambah Uncensored SETELAH judul, sebelum resolusi
        if ($uncenTag) {
            $final += " $uncenTag"
        }

        if ($reso) { $final += " $reso" }

        # Bersihin tanda "-" ekstra & spasi berlebih
        if (-not $code) {  # hanya normalisasi kalau gak ada kode
            $final = $final -replace '\s*-\s*', ' - '          # normalisasi "-"
        }
        $final = $final -replace '^\s*-+\s*', ''               # hapus "-" di awal
        $final = $final -replace ' - - ', ' - '                # hapus "-" dobel kalau kelewat
        $final = $final -replace '\s{2,}', ' '                 # spasi dobel jadi satu
        $final = $final.Trim(' -')                             # hapus "-" atau spasi di ujung

        # 11. Keyword enforcer
        foreach ($k in $keywordList) {
            $esc = [regex]::Escape($k)
            $final = [regex]::Replace($final, "(?i)\b$esc\b", $k)
        }

        $newName = $final + $ext

        # 12. Duplikat check – kalau duplikat, tetep catat, tapi pindah ke Real kalau punya kode JAV
        $key = $newName.ToLower()
        $titleKey = $final.ToLower() -replace '\s*\((\d+|copy|copi|dup|v\d+|ver\s*\d+)\)\s*$','' -replace '\s*\b(copy|copi|duplicate|dup|v\d+)\b\s*$',''
        $titleKey = ($titleKey -replace '\s{2,}',' ').Trim()
        $isDuplicate = $false
        if ($titleRegistry.ContainsKey($titleKey)) {
            Write-Host "Judul duplikat (judul.txt): '$original'" -ForegroundColor Cyan
            $isDuplicate = $true
            $duplicateMoveCount++
        }
        if ($seenTitles.ContainsKey($key)) {
            Write-Host "Duplicate nama file: '$original'" -ForegroundColor Cyan
            $isDuplicate = $true
            $duplicateMoveCount++
        }
        $seenTitles[$key] = $true

        if ($original -ceq $newName) {
            $skipCleanCount++
        } else {
            Rename-Item -LiteralPath $_.FullName -NewName $newName -ErrorAction Stop
            Write-Host "[RENAMED] $original -> $newName" -ForegroundColor Green
            $renamedCount++
        }

        # 13. Pindah file berdasarkan prioritas (fix permanen)
        if ($code) {
            # Prioritas tertinggi: punya kode JAV → masuk Real (termasuk cosplay, JAV, dll)
            $targetFolder = Join-Path $currentDir "Real"
            if (-not (Test-Path $targetFolder)) {
                New-Item -ItemType Directory -Path $targetFolder | Out-Null
            }
            $targetPath = Join-Path $targetFolder $newName
            Move-Item -LiteralPath (Join-Path $currentDir $newName) -Destination $targetPath -Force
            Write-Host "[MOVED] $newName → folder Real" -ForegroundColor Yellow
            $realCount++
        }
        elseif ($isDuplicate) {
            # Prioritas kedua: duplikat tapi gak punya kode JAV → masuk _DUPLICATE
            $targetPath = Join-Path $dupFolder $newName
            Move-Item -LiteralPath (Join-Path $currentDir $newName) -Destination $targetPath -Force
            Write-Host "[MOVED] $newName → folder _DUPLICATE (no code JAV)" -ForegroundColor DarkCyan
        }
        # Fitur baru: pindah ke Lainnya kalau ada snapsave ATAU gak ada nekopoi di nama asli
        else {
            $lowerOriginal = $original.ToLower()
            if ($lowerOriginal -match '\b(snapsave|fbdownloader|fbdownload)\b' -or $lowerOriginal -notmatch '\b(nekopoi|nekpoi|nek poi|neko poi)\b') {
                $targetFolder = Join-Path $currentDir "Lainnya"
                if (-not (Test-Path $targetFolder)) {
                    New-Item -ItemType Directory -Path $targetFolder | Out-Null
                }
                $targetPath = Join-Path $targetFolder $newName
                Move-Item -LiteralPath (Join-Path $currentDir $newName) -Destination $targetPath -Force
                Write-Host "[MOVED] $newName → folder Lainnya (snapsave atau non-nekopoi)" -ForegroundColor Magenta
                $lainnyaCount++
            }
        }

        if (-not $titleRegistry.ContainsKey($titleKey)) {
            Add-TitleRegistry -Title $final
            $titleRegistry[$titleKey] = $true
        }
    }
    catch {
        Write-Host "Gagal proses '$original' : $_" -ForegroundColor Red
    }
}

Sort-TitleRegistry

if ($renamedCount -eq 0 -and $duplicateMoveCount -eq 0 -and $titleNullCount -eq 0) {
    Write-Host "Semua file udah rapi bro, Nothing to cleanup lagi~" -ForegroundColor Green
} else {
    Write-Host "Masih ada yang diberesin, tapi udah aman kok" -ForegroundColor Cyan
}

Write-Host "`n=========== RINGKASAN ===========" -ForegroundColor Magenta
Write-Host "✔ Di-rename    : $renamedCount file" -ForegroundColor Green
Write-Host "⇰ Sudah rapi   : $skipCleanCount file" -ForegroundColor Cyan
Write-Host "↻ Judul kosong : $titleNullCount file" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Magenta
Write-Host "`n===========  OUTPUT  ===========" -ForegroundColor Magenta
Write-Host "✔ Real         : $realCount file" -ForegroundColor Green
Write-Host "⇰ Lainnya      : $lainnyaCount file" -ForegroundColor Cyan
Write-Host "⇲ Duplicate    : $duplicateMoveCount file" -ForegroundColor Red
Write-Host "=================================" -ForegroundColor Magenta