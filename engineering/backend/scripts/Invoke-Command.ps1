param([Parameter(Mandatory = $true)][string]$SpecPath)
$ErrorActionPreference = 'Stop'
$spec = Get-Content -LiteralPath $SpecPath -Raw | ConvertFrom-Json
Set-Location -LiteralPath $spec.workingDirectory
if ($spec.environment) {
    foreach ($item in $spec.environment.PSObject.Properties) {
        [Environment]::SetEnvironmentVariable($item.Name, [string]$item.Value, 'Process')
    }
}
$arguments = @($spec.arguments | ForEach-Object { [string]$_ })
try {
    & ([string]$spec.executable) @arguments
    if ($null -ne $LASTEXITCODE) { exit $LASTEXITCODE }
    if (-not $?) { exit 1 }
    exit 0
} catch {
    Write-Error $_
    exit 1
}
