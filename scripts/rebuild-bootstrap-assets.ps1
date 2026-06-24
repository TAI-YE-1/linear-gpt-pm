param(
    [string]$BootstrapPath = "scripts\bootstrap-ai-sop.ps1"
)

$ErrorActionPreference = "Stop"

$assetPaths = @(
    "AGENTS.md",
    ".codex\skills\openspec-superpowers-sop\SKILL.md",
    "docs\ai-sop-usage.md",
    "docs\prompts\00-router.md",
    "docs\prompts\01-propose.md",
    "docs\prompts\02-subagent-plan.md",
    "docs\prompts\03-apply.md",
    "docs\prompts\04-verify.md",
    "docs\prompts\05-review-archive.md",
    "scripts\new-ai-change-prompt.ps1",
    "scripts\rebuild-bootstrap-assets.ps1"
)

foreach ($assetPath in $assetPaths) {
    if (-not (Test-Path -LiteralPath $assetPath)) {
        throw "Missing asset: $assetPath"
    }
}

if (-not (Test-Path -LiteralPath $BootstrapPath)) {
    throw "Bootstrap script not found: $BootstrapPath"
}

Add-Type -AssemblyName System.IO.Compression | Out-Null

$zipStream = New-Object System.IO.MemoryStream
try {
    $archive = New-Object System.IO.Compression.ZipArchive($zipStream, [System.IO.Compression.ZipArchiveMode]::Create, $true)
    try {
        foreach ($assetPath in $assetPaths) {
            $entryName = $assetPath.Replace("\", "/")
            $entry = $archive.CreateEntry($entryName, [System.IO.Compression.CompressionLevel]::Optimal)
            $entryStream = $entry.Open()
            try {
                $bytes = [System.IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $assetPath))
                $entryStream.Write($bytes, 0, $bytes.Length)
            } finally {
                $entryStream.Dispose()
            }
        }
    } finally {
        $archive.Dispose()
    }

    $base64 = [Convert]::ToBase64String($zipStream.ToArray())
} finally {
    $zipStream.Dispose()
}

$lines = [System.Collections.Generic.List[string]]::new()
$lines.AddRange([string[]](Get-Content -Encoding UTF8 $BootstrapPath))

$startIndex = -1
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -eq "    `$zipBase64 = @'") {
        $startIndex = $i
        break
    }
}

if ($startIndex -lt 0) {
    throw "Could not find embedded asset block start in $BootstrapPath"
}

$endIndex = -1
for ($i = $startIndex + 1; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -eq "'@") {
        $endIndex = $i
        break
    }
}

if ($endIndex -lt 0) {
    throw "Could not find embedded asset block end in $BootstrapPath"
}

$updatedLines = [System.Collections.Generic.List[string]]::new()
if ($startIndex -gt 0) {
    $updatedLines.AddRange([string[]]$lines.GetRange(0, $startIndex + 1))
} else {
    $updatedLines.Add($lines[0])
}
$updatedLines.Add($base64)
$updatedLines.AddRange([string[]]$lines.GetRange($endIndex, $lines.Count - $endIndex))

$updatedLines | Set-Content -Encoding UTF8 $BootstrapPath

Write-Host "[ok] Embedded $($assetPaths.Count) assets into $BootstrapPath"
