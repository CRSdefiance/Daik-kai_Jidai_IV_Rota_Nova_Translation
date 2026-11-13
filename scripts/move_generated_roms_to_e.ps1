param()

$ErrorActionPreference = 'Stop'
$repositoryRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path.TrimEnd('\')
$approvedDestination = 'E:\Rota Nova translations'
$destinationRoot = Join-Path $approvedDestination 'Generated'
$receiptPath = Join-Path $repositoryRoot 'translations\generated_rom_storage_move.json'
$cleanPath = Join-Path $repositoryRoot 'work\clean.nds'
$cleanHash = (Get-FileHash -LiteralPath $cleanPath -Algorithm SHA256).Hash

function Assert-ContainedPath([string]$Path, [string]$Root) {
    $absolute = [IO.Path]::GetFullPath($Path)
    $prefix = [IO.Path]::GetFullPath($Root).TrimEnd('\') + '\'
    if (-not $absolute.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Path is outside the approved root: $absolute"
    }
    return $absolute
}

if (Test-Path -LiteralPath $receiptPath) {
    throw 'A migration receipt already exists. Inspect it before starting another migration.'
}
New-Item -ItemType Directory -Path $destinationRoot -Force | Out-Null
$folders = @((Join-Path $repositoryRoot 'out'))
$workPath = Join-Path $repositoryRoot 'work'
foreach ($folder in Get-ChildItem -LiteralPath $workPath -Directory) {
    if (Get-ChildItem -LiteralPath $folder.FullName -Recurse -File -Filter '*.nds' | Select-Object -First 1) {
        $folders += $folder.FullName
    }
}
$rootRoms = @(Get-ChildItem -LiteralPath $workPath -File -Filter '*.nds' | Where-Object { $_.Name -ne 'clean.nds' })
$plan = @()
foreach ($folder in $folders) {
    $source = Assert-ContainedPath $folder $repositoryRoot
    if ((Get-Item -LiteralPath $source).Attributes -band [IO.FileAttributes]::ReparsePoint) {
        throw "Source folder already has a link: $source"
    }
    if (Get-ChildItem -LiteralPath $source -Recurse -Force -Attributes ReparsePoint | Select-Object -First 1) {
        throw "Source contains directory/file links; inspect before moving: $source"
    }
    $relative = $source.Substring($repositoryRoot.Length + 1)
    $target = Assert-ContainedPath (Join-Path $destinationRoot $relative) $approvedDestination
    if (Test-Path -LiteralPath $target) { throw "Destination exists: $target" }
    $plan += [pscustomobject]@{source=$source;destination=$target;relative=$relative;status='pending';verifiedFiles=0;verifiedRoms=0}
}
$migration = [pscustomobject]@{
    format='dk4-generated-rom-storage-move-v1'
    startedUtc=[DateTime]::UtcNow.ToString('o')
    status='running'
    repositoryRoot=$repositoryRoot
    destinationRoot=$destinationRoot
    originalCleanRom=$cleanPath
    originalCleanSha256=$cleanHash
    packages=$plan
    rootRoms=@()
    roms=@()
}
function Save-Receipt {
    $migration | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $receiptPath -Encoding utf8
}
Save-Receipt
$totalRoms = 0
foreach ($package in $plan) {
    Write-Output "Copying package: $($package.relative)"
    $package.status = 'copying'
    Save-Receipt
    $sourceFiles = @(Get-ChildItem -LiteralPath $package.source -Recurse -Force -File)
    New-Item -ItemType Directory -Path (Split-Path -Parent $package.destination) -Force | Out-Null
    Copy-Item -LiteralPath $package.source -Destination $package.destination -Recurse -Force
    $targetFiles = @(Get-ChildItem -LiteralPath $package.destination -Recurse -Force -File)
    if ($sourceFiles.Count -ne $targetFiles.Count) { throw "File count changed: $($package.relative)" }
    $package.status = 'verifying'
    Save-Receipt
    foreach ($file in $sourceFiles) {
        $relativeFile = $file.FullName.Substring($package.source.Length + 1)
        $targetFile = Assert-ContainedPath (Join-Path $package.destination $relativeFile) $approvedDestination
        if (-not (Test-Path -LiteralPath $targetFile -PathType Leaf)) { throw "Missing copy: $targetFile" }
        if ($file.Length -ne (Get-Item -LiteralPath $targetFile).Length) { throw "Length differs: $targetFile" }
        $before = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash
        $after = (Get-FileHash -LiteralPath $targetFile -Algorithm SHA256).Hash
        if ($before -ne $after) { throw "Copy hash differs: $targetFile" }
        $package.verifiedFiles++
        if ($file.Extension -ieq '.nds') {
            $migration.roms += [pscustomobject]@{originalPath=$file.FullName;destination=$targetFile;bytes=$file.Length;sha256=$after}
            $package.verifiedRoms++
            $totalRoms++
            if ($totalRoms % 50 -eq 0) { Write-Output "Verified ROM copies: $totalRoms" }
        }
    }
    $backup = Assert-ContainedPath ($package.source + '.rom-move-backup-' + [Guid]::NewGuid().ToString('N')) $repositoryRoot
    $package.status = 'copies_verified'
    Save-Receipt
    Move-Item -LiteralPath $package.source -Destination $backup
    try {
        New-Item -ItemType Junction -Path $package.source -Target $package.destination | Out-Null
    } catch {
        Move-Item -LiteralPath $backup -Destination $package.source
        throw
    }
    $resolvedBackup = (Resolve-Path -LiteralPath $backup).Path
    $null = Assert-ContainedPath $resolvedBackup $repositoryRoot
    if ((Get-Item -LiteralPath $resolvedBackup).Attributes -band [IO.FileAttributes]::ReparsePoint) {
        throw "Backup unexpectedly became a link: $resolvedBackup"
    }
    # Copies and all hashes are verified before this workspace-only cleanup.
    Remove-Item -LiteralPath $resolvedBackup -Recurse -Force
    $package.status = 'moved_with_compatibility_junction'
    Save-Receipt
    Write-Output "Moved $($package.relative): $($package.verifiedRoms) ROMs; all $($package.verifiedFiles) file hashes verified."
}
foreach ($file in $rootRoms) {
    $source = Assert-ContainedPath $file.FullName $repositoryRoot
    $target = Assert-ContainedPath (Join-Path $destinationRoot ('work\' + $file.Name)) $approvedDestination
    if (Test-Path -LiteralPath $target) { throw "Destination exists: $target" }
    Copy-Item -LiteralPath $source -Destination $target
    $before = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
    $after = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash
    if ($before -ne $after) { throw "Copy hash differs: $target" }
    Remove-Item -LiteralPath $source
    $row = [pscustomobject]@{originalPath=$source;destination=$target;bytes=$file.Length;sha256=$after}
    $migration.rootRoms += $row
    $migration.roms += $row
    $totalRoms++
    Save-Receipt
}
if ((Get-FileHash -LiteralPath $cleanPath -Algorithm SHA256).Hash -ne $cleanHash) {
    throw 'Original clean ROM changed.'
}
$remaining = @(Get-ChildItem -LiteralPath $repositoryRoot -Recurse -File -Filter '*.nds' |
    Where-Object { $_.FullName -notmatch '[\\/]sources[\\/]' -and $_.FullName -ne $cleanPath })
if ($remaining.Count) { throw "Generated ROMs remain outside migrated folders: $($remaining.FullName -join ', ')" }
$migration.status = 'complete'
$migration | Add-Member -NotePropertyName completedUtc -NotePropertyValue ([DateTime]::UtcNow.ToString('o'))
$migration | Add-Member -NotePropertyName generatedRomsMoved -NotePropertyValue $totalRoms
Save-Receipt
Write-Output "Migration complete: $totalRoms generated ROMs physically on E; original clean ROM retained."
(Get-PSDrive -Name C | Select-Object Free) | ConvertTo-Json
