$ErrorActionPreference = 'Stop'

# ---- CONFIG ----
$Root  = 'Y:\VIDEOS\1190\Video'
$Dates = @('2024-05-28','2024-05-29','2024-05-30')
# ---------------

# Ensure ffmpeg exists
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    Write-Error "FFmpeg not found in PATH. Make sure it's installed and in PATH."
}

foreach ($d in $Dates) {
    $dir = Join-Path $Root $d
    if (-not (Test-Path $dir)) {
        Write-Host "(Skip) Folder not found: $dir"
        continue
    }

    # Create an "output" subfolder inside the date folder
    $outDir = Join-Path $dir "output"
    if (-not (Test-Path $outDir)) {
        New-Item -ItemType Directory -Path $outDir | Out-Null
    }

    Write-Host "=== Scanning $dir ==="
    Get-ChildItem -Path $dir -Filter *.asf -Recurse | ForEach-Object {
        $in  = $_.FullName
        $out = Join-Path $outDir ($_.BaseName + '.mp4')

        Write-Host "Converting: $in"
        & ffmpeg -y -i $in -c:v libx264 -crf 20 -preset medium -c:a aac -b:a 160k -movflags +faststart $out
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "Failed: $in"
        } else {
            Write-Host "  > Done: $out"
        }
    }
}
Write-Host "All done."
