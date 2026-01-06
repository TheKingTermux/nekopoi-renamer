$videoExt = ".mp4",".mkv",".mov",".webm"
$seenTitles = @{}
$renamedCount = 0
$skipCleanCount = 0
$duplicateMoveCount = 0
$titleNullCount = 0

# Folder pembuangan duplikat
$dupFolder = "_DUPLICATE"
if (-not (Test-Path $dupFolder)) {
    New-Item -ItemType Directory -Name $dupFolder | Out-Null
}

# Load author whitelist
$authorFile = "author.txt"
$authorList = @()
if (Test-Path $authorFile) {
    $authorList = Get-Content $authorFile | Where-Object { $_.Trim() -ne "" }
}

# Load keyword whitelist
$keywordFile = "keyword.txt"
$keywordList = @()
if (Test-Path $keywordFile) {
    $keywordList = Get-Content $keywordFile | Where-Object { $_.Trim() -ne "" }
}

# Load title registry
$titleFile = "judul.txt"
$titleRegistry = @{}
if (Test-Path $titleFile) {
    Get-Content $titleFile | ForEach-Object {
        $k = ($_ -replace '\s+',' ').Trim().ToLower()
        if ($k) { $titleRegistry[$k] = $true }
    }
}

# Save title registry
function Add-TitleRegistry {
    param (
        [string]$Title,
        [string]$File = "judul.txt"
    )

    Add-Content -Path $File -Value "`r`n$Title"
}

# Automatic sort title registry
function Sort-TitleRegistry {
    param (
        [string]$File = "judul.txt"
    )

    if (-not (Test-Path $File)) { return }

    $sorted = Get-Content $File |
        Where-Object { $_.Trim() -ne "" } |
        Sort-Object { $_.ToLower() } -Unique

    Set-Content -Path $File -Value $sorted
}

# Scan semua file
Get-ChildItem -File | Where-Object {
    $videoExt -contains $_.Extension.ToLower()
} | ForEach-Object {

    $original = $_.Name
    $name = $_.BaseName
    $ext  = $_.Extension

    # reset metadata
    $reso = ""
    $dim = ""
    $studio = ""
    $code = ""
    $hasAuthor = $false

    try {
        # =============================
        # 1 HAPUS DOMAIN / NEKOPOI
        # =============================
        $name = $name -replace '(?i)nekopoi', ''
        $name = $name -replace '(?i)\.(care|fun|tv|id|io|xyz|site|club|live|net|org|cc|me|pw|biz|info|asia|us|uk|pro|lol|trade|host|band|top)\b', ''

        # =============================
        # 2 RESOLUTION (ambil terakhir)
        # =============================
        if ($name -match '(\d{3,4})[pP](?!.*\d{3,4}[pP])') {
            $reso = "$($matches[1])P"
            $name = $name -replace "$($matches[1])[pP]", ''
        }

        # =============================
        # 3 DIMENSION (LIVE2D / L2D / 2D / 3D)
        # =============================
        if ($name -match '(?i)\b(LIVE2D|L2D)\b') {
            $dim = "LIVE2D"
            $name = $name -replace '(?i)\b(LIVE2D|L2D)\b',''
        } elseif ($name -match '(?i)\b(2D|3D)\b') {
            $dim = $matches[1].ToUpper()
            $name = $name -replace '(?i)\b(2D|3D)\b',''
        }

        # =============================
        # 4 AUTHOR — By Author
        # =============================
        if ($name -match '(?i)\bBy\s+([^\[\]\(\)\-]+)') {
            $studio = $matches[1].Trim()
            $name = $name -replace '(?i)\bBy\s+[^\[\]\(\)\-]+',''
            $hasAuthor = $true
        }

        # =============================
        # 5 AUTHOR — whitelist prefix
        # =============================
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

        # =============================
        # 6 CLEAN SYMBOL
        # =============================
        $name = $name -replace '[\[\]{}()_]+',' '

        # =============================
        # 7 CODE JAV
        # =============================
        $patterns = @(
            '(?i)FC2[-_\s]*PPV[-_\s]*(\d{3,9})',
            '(?i)FC2[-_\s]*(\d{3,9})',
            '(?i)(KBJ)[-_\s]?(\d{6,12})',
            '(?i)(CN)[-_\s]?(\d{6,12})',
            '(?i)(MD)[-_\s]?(\d{3,6})(-\d+)?',
            '\b([A-Z]{2,5})[-_\s]?(\d{2,5})(-\d+)?\b'
        )

        foreach ($pat in $patterns) {
            if ($name -match $pat) {
                if ($matches.Count -ge 3) {
                    $codeExtract = "$($matches[1].ToUpper())-$($matches[2])$($matches[3])"
                } else {
                    $codeExtract = $matches[0].ToUpper()
                }
                $code = ($code, $codeExtract) -join " "
                $name = $name -replace $pat,''
            }
        }

        # =============================
        # 8 NORMALIZE
        # =============================
        $name = ($name -replace '\s{2,}',' ').Trim()
        $code = ($code -replace '\s{2,}',' ').Trim()

        $textInfo = (Get-Culture).TextInfo
        $name = $textInfo.ToTitleCase($name.ToLower())

        # =============================
        # 9 FALLBACK
        # =============================
        if ([string]::IsNullOrWhiteSpace($name)) {
            Write-Host "Judul kosong → fallback baseName: $original" -ForegroundColor Yellow
            $name = $textInfo.ToTitleCase($_.BaseName.ToLower())
            $titleNullCount++
        }

        # =============================
        # 10 BUILD FINAL
        # =============================
        $final = ""
        if ($code)   { $final += "$code " }
        if ($dim)    { $final += "$dim " }
        if ($studio) { $final += "$studio - " }
        $final += $name
        if ($reso)   { $final += " $reso" }

        # =============================
        # 10.2 FINAL NORMALIZATION
        # =============================
        $final = $final -replace '\s*(-\s*){2,}', ' - '
        $final = $final -replace '\s{2,}', ' '
        $final = $final.Trim(' -')

        # =============================
        # FINAL KEYWORD ENFORCER (ANTI TITLECASE)
        # =============================
        foreach ($k in $keywordList) {
            $esc = [regex]::Escape($k)
            $final = [regex]::Replace(
                $final,
                "(?i)\b$esc\b",
                $k
            )
        }

        $newName = ($final + $ext)

        # =============================
        # 10.3 TITLE REGISTRY CHECK (judul.txt)
        # =============================
        $key = $newName.ToLower()
        $titleKey = $final.ToLower()

        # buang suffix duplikat umum
        $titleKey = $titleKey -replace '\s*\((\d+|0\d+|copy|copi|dup|v\d+|ver\s*\d+)\)\s*$',''
        $titleKey = $titleKey -replace '\s*\b(copy|copi|duplicate|dup|v\d+)\b\s*$',''

        # normalize space
        $titleKey = ($titleKey -replace '\s{2,}',' ').Trim()

        if ($titleRegistry.ContainsKey($titleKey)) {
            Write-Host "Judul duplikat (judul.txt) → SKIP: '$original'" -ForegroundColor Cyan
            Move-Item $_.FullName $dupFolder -Force
            $skipCleanCount++
            return
        }

        # =============================
        # 11 DUPLICATE
        # =============================
        if ($seenTitles.ContainsKey($key)) {
            Write-Host "Duplicate → dipindah: '$original'" -ForegroundColor Cyan
            Move-Item $_.FullName $dupFolder -Force
            $duplicateMoveCount++
            return
        }

        $seenTitles[$key] = $true

        # =============================
        # 12 RENAME + SAVE TO JUDUL.TXT
        # =============================
        if ($original -ceq $newName) {
            $skipCleanCount++
            return
        }

        Rename-Item -LiteralPath $_.FullName -NewName $newName -ErrorAction Stop
        Write-Host "[RENAMED] $original  ->  $newName" -ForegroundColor Green
        if (-not $titleRegistry.ContainsKey($titleKey)) {
            Add-TitleRegistry -Title $final
            $titleRegistry[$titleKey] = $true
        }
        $renamedCount++
        return
    }
    catch { 
        Write-Host "Gagal proses '$original' : $_" -ForegroundColor Red
    }
}

Sort-TitleRegistry

    if ($renamedCount -eq 0 -and $duplicateMoveCount -eq 0 -and $titleNullCount -eq 0) { 
        Write-Host "Semua file udah rapi bro, Nothing to cleanup lagi~"  -ForegroundColor Green
    } 
    else { 
        Write-Host "Masih ada yang diberesin, tapi udah aman kok" -ForegroundColor Cyan
    }

Write-Host "`n=========== RINGKASAN ===========" -ForegroundColor Magenta
Write-Host "✔ Di-rename        : $renamedCount file" -ForegroundColor Green
Write-Host "⇰ Sudah rapi       : $skipCleanCount file" -ForegroundColor Cyan
Write-Host "⇲ Duplicate pindah : $duplicateMoveCount file" -ForegroundColor Red
Write-Host "↻ Judul kosong     : $titleNullCount file" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Magenta