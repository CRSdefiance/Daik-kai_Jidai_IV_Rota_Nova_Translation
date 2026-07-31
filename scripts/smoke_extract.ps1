param(
    [Parameter(Mandatory = $true)][string]$Rom
)
$ErrorActionPreference = "Stop"
dk4tool manifest $Rom --out work/manifest.json
dk4tool extract-files $Rom --out work/files
dk4tool scan $Rom --out work/scan_report.json

