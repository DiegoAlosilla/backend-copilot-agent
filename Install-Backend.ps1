param(
    [Parameter(Mandatory = $true)][string]$RepositoryPath,
    [switch]$PlanOnly,
    [switch]$SupportOnly
)
$ErrorActionPreference = 'Stop'
& (Join-Path $PSScriptRoot 'distribution/Install-Managed.ps1') @PSBoundParameters
