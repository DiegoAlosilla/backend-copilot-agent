param(
    [Parameter(Mandatory = $true)][string]$RepositoryPath,
    [switch]$PlanOnly,
    [switch]$SupportOnly
)
$ErrorActionPreference = 'Stop'
$packageRoot = Split-Path -Parent $PSScriptRoot
$targetRoot = (Resolve-Path -LiteralPath $RepositoryPath).Path
$gitRoot = & git -C $targetRoot rev-parse --show-toplevel
if ($LASTEXITCODE -ne 0) { throw 'El destino debe ser un repositorio Git.' }
if ((Resolve-Path -LiteralPath $gitRoot).Path -ne $targetRoot) { throw 'Indica la raíz del repositorio.' }
if ($targetRoot -eq $packageRoot) { throw 'El paquete no es el microservicio destino.' }
$version = (Get-Content -LiteralPath (Join-Path $packageRoot 'plugin.json') -Raw -Encoding UTF8 |
    ConvertFrom-Json).version

function Assert-TargetPath([string]$Path) {
    $resolved = [IO.Path]::GetFullPath($Path)
    if (-not $resolved.StartsWith($targetRoot.TrimEnd('\', '/') + [IO.Path]::DirectorySeparatorChar,
            [StringComparison]::OrdinalIgnoreCase)) { throw 'Destino fuera del repositorio.' }
    $current = $resolved
    while ($current.Length -ge $targetRoot.Length) {
        if ((Test-Path -LiteralPath $current) -and
            ((Get-Item -LiteralPath $current).Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            throw "No instalar a través de symlink/junction: $current"
        }
        if ($current -eq $targetRoot) { break }
        $current = Split-Path -Parent $current
    }
}
function Hash-Text([string]$Value) {
    $algorithm = [Security.Cryptography.SHA256]::Create()
    try {
        $normalized = $Value.Replace("`r`n", "`n")
        return ([BitConverter]::ToString($algorithm.ComputeHash([Text.Encoding]::UTF8.GetBytes($normalized)))).Replace('-', '')
    } finally { $algorithm.Dispose() }
}

$metadataPath = Join-Path $targetRoot '.assistant-local/backend/installation.json'
Assert-TargetPath $metadataPath
$previous = @{}
if (Test-Path -LiteralPath $metadataPath) {
    $stored = Get-Content -LiteralPath $metadataPath -Raw -Encoding UTF8 | ConvertFrom-Json
    foreach ($item in $stored.files.PSObject.Properties) { $previous[$item.Name] = $item.Value }
}
$nextMetadata = @{}
foreach ($name in $previous.Keys) { $nextMetadata[$name] = $previous[$name] }
$sourceFiles = @(Get-ChildItem -LiteralPath (Join-Path $packageRoot 'engineering/backend') -Recurse -File |
    Where-Object { $_.FullName -notmatch '[\\/]__pycache__[\\/]' })
if (-not $SupportOnly) {
    foreach ($folder in @('agents', 'skills')) {
        $sourceFiles += Get-ChildItem -LiteralPath (Join-Path $packageRoot $folder) -Recurse -File
    }
    $sourceFiles += Get-Item -LiteralPath (Join-Path $packageRoot 'rules/backend.instructions.md')
}
$actions = @()
$conflicts = @()
$start = '<!-- backend-package:start -->'
$end = '<!-- backend-package:end -->'
$pattern = '(?s)<!-- backend-package:start(?: v[^>]+)? -->.*?<!-- backend-package:end -->'
foreach ($source in $sourceFiles) {
    $relative = $source.FullName.Substring($packageRoot.Length).TrimStart('\', '/').Replace('\', '/')
    if ($relative.StartsWith('agents/') -or $relative.StartsWith('skills/')) {
        $relative = '.github/' + $relative
    } elseif ($relative -eq 'rules/backend.instructions.md') {
        $relative = '.github/copilot-instructions.md'
    }
    $destination = [IO.Path]::GetFullPath((Join-Path $targetRoot $relative))
    Assert-TargetPath $destination
    $sourceHash = (Get-FileHash -LiteralPath $source.FullName).Hash
    if ($relative -eq '.github/copilot-instructions.md') {
        $incoming = Get-Content -LiteralPath $source.FullName -Raw -Encoding UTF8
        $incoming = [regex]::Replace($incoming, '\A---\r?\n.*?\r?\n---\r?\n\s*', '', [Text.RegularExpressions.RegexOptions]::Singleline)
        $block = $start + "`n" + $incoming + "`n" + $end
        $blockHash = Hash-Text $block
        if (Test-Path -LiteralPath $destination) {
            $existingText = Get-Content -LiteralPath $destination -Raw -Encoding UTF8
            $matches = [regex]::Matches($existingText, $pattern)
            if ($matches.Count -gt 1) { $conflicts += $destination; continue }
            if ($matches.Count -eq 1) {
                $currentHash = Hash-Text $matches[0].Value
                if ($currentHash -ne $blockHash) {
                    if ($previous.ContainsKey($relative) -and $currentHash -eq $previous[$relative].hash) {
                        $newText = $existingText.Substring(0, $matches[0].Index) + $block +
                            $existingText.Substring($matches[0].Index + $matches[0].Length)
                        $actions += [pscustomobject]@{ Destination = $destination; Action = 'UPDATE-BLOCK'; Text = $newText; Source = $null }
                    } else { $conflicts += $destination; continue }
                }
            } elseif ($existingText.Trim() -eq $incoming.Trim()) {
                $actions += [pscustomobject]@{ Destination = $destination; Action = 'WRAP-BLOCK'; Text = $block + "`n"; Source = $null }
            } else {
                $actions += [pscustomobject]@{ Destination = $destination; Action = 'APPEND-BLOCK'; Text = $existingText + "`n" + $block + "`n"; Source = $null }
            }
        } else {
            $actions += [pscustomobject]@{ Destination = $destination; Action = 'CREATE-BLOCK'; Text = $block + "`n"; Source = $null }
        }
        $nextMetadata[$relative] = @{ hash = $blockHash; kind = 'instructions-block' }
        continue
    }
    if (Test-Path -LiteralPath $destination) {
        $destinationHash = (Get-FileHash -LiteralPath $destination).Hash
        if ($relative -in @('engineering/backend/repository-profile.json', 'engineering/backend/quality-policy.json')) {
            continue
        }
        if ($destinationHash -ne $sourceHash) {
            if ($previous.ContainsKey($relative) -and $destinationHash -eq $previous[$relative].hash) {
                $actions += [pscustomobject]@{ Source = $source.FullName; Destination = $destination; Action = 'UPDATE'; Text = $null }
            } else { $conflicts += $destination; continue }
        }
    } else {
        $actions += [pscustomobject]@{ Source = $source.FullName; Destination = $destination; Action = 'CREATE'; Text = $null }
    }
    $nextMetadata[$relative] = @{ hash = $sourceHash; kind = 'file' }
}
if ($conflicts.Count) {
    $conflicts | ForEach-Object { Write-Output "CONFLICT: $_" }
    throw 'No se modificó ningún archivo. Hay personalizaciones o una instalación sin huellas; integra esos cambios manualmente.'
}
$actions | ForEach-Object { Write-Output ($_.Action + ': ' + $_.Destination) }
if ($PlanOnly) { Write-Output 'PLAN_ONLY: no se modificó el repositorio.'; exit 0 }
foreach ($action in $actions) {
    New-Item -ItemType Directory -Path (Split-Path -Parent $action.Destination) -Force | Out-Null
    if ($null -ne $action.Text) {
        [IO.File]::WriteAllText($action.Destination, $action.Text, [Text.UTF8Encoding]::new($false))
    } else { Copy-Item -LiteralPath $action.Source -Destination $action.Destination }
}
$excludeFile = & git -C $targetRoot rev-parse --path-format=absolute --git-path info/exclude
if ($LASTEXITCODE -ne 0) { throw 'No se pudo resolver git info/exclude.' }
New-Item -ItemType Directory -Path (Split-Path -Parent $excludeFile) -Force | Out-Null
$excludeText = if (Test-Path -LiteralPath $excludeFile) { Get-Content -LiteralPath $excludeFile -Raw -Encoding UTF8 } else { '' }
if (-not ($excludeText -match '(?m)^/\.assistant-local/\s*$')) {
    [IO.File]::AppendAllText($excludeFile, "`n/.assistant-local/`n", [Text.UTF8Encoding]::new($false))
}
New-Item -ItemType Directory -Path (Split-Path -Parent $metadataPath) -Force | Out-Null
$metadata = @{ schemaVersion = 1; packageVersion = $version; files = $nextMetadata }
[IO.File]::WriteAllText($metadataPath, ($metadata | ConvertTo-Json -Depth 6) + "`n", [Text.UTF8Encoding]::new($false))
Write-Output "INSTALLED $version : soporte preparado; no se ejecutó Maven ni acciones remotas."
