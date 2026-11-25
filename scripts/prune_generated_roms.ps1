param(
    [ValidateRange(1, 365)][int]$KeepRecentDays = 3,
    [string]$ApplyPlan
)

$ErrorActionPreference = 'Stop'
$repository = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$storage = 'E:\Rota Nova translations'
$generated = Join-Path $storage 'Generated'
$audit = Join-Path $repository 'work\rom_retention'
$zone = [TimeZoneInfo]::FindSystemTimeZoneById('US Eastern Standard Time')

function Read-Json([string]$File) {
    Get-Content -LiteralPath $File -Raw | ConvertFrom-Json
}
function Write-Json($Value, [string]$File) {
    $Value | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $File -Encoding utf8
}
function Assert-RomPath([string]$File) {
    $full = [IO.Path]::GetFullPath($File)
    $prefix = $storage.TrimEnd('\') + '\'
    if (-not $full.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase) -or
        [IO.Path]::GetExtension($full) -ine '.nds') {
        throw "Not a generated ROM in the approved storage folder: $full"
    }
    # Only the top-level handoff folder and Generated are in scope.
    if ([IO.Path]::GetDirectoryName($full) -ine $storage -and
        -not $full.StartsWith($generated + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw "Outside the generated archive: $full"
    }
    $item = Get-Item -LiteralPath $full
    while ($item.FullName -ine $storage) {
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
            throw "Refusing to traverse a link: $($item.FullName)"
        }
        $item = Get-Item -LiteralPath (Split-Path -Parent $item.FullName)
    }
    if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
        throw 'The storage root must be a physical directory.'
    }
    return $full
}
function Get-Roms {
    @(Get-ChildItem -LiteralPath $generated -Recurse -File -Filter '*.nds') +
        @(Get-ChildItem -LiteralPath $storage -File -Filter '*.nds')
}
function Get-GuardRecords {
    $registry = Read-Json (Join-Path $repository 'translations\release_stack.json')
    $base = $registry.canonical_baseline
    @(
        [pscustomobject]@{path=(Join-Path $repository 'work\clean.nds');sha256='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'},
        [pscustomobject]@{path=(Join-Path $repository $base.path);sha256=$base.sha256},
        [pscustomobject]@{path=(Join-Path $repository $base.previous_baseline.path);sha256=$base.previous_baseline.sha256}
    )
}
function Assert-Guards($Records) {
    foreach ($row in $Records) {
        if ((Get-FileHash -LiteralPath $row.path -Algorithm SHA256).Hash -ine $row.sha256) {
            throw "Protected source/baseline hash mismatch: $($row.path)"
        }
    }
}

New-Item -ItemType Directory -Path $audit -Force | Out-Null
if ($ApplyPlan) {
    $planPath = [IO.Path]::GetFullPath($ApplyPlan)
    if (-not $planPath.StartsWith($audit + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Apply only a saved plan from work\rom_retention.'
    }
    $plan = Read-Json $planPath
    if ($plan.format -ne 'dk4-rom-retention-v1' -or $plan.storageRoot -ine $storage) {
        throw 'Unrecognized retention plan.'
    }
    $resultPath = $planPath -replace '\.json$', '.result.json'
    $journalPath = $planPath -replace '\.json$', '.journal.jsonl'
    if ((Test-Path -LiteralPath $resultPath) -or (Test-Path -LiteralPath $journalPath)) {
        throw 'This plan has already been started. Inspect its result/journal; create a new plan.'
    }
    $guards = @(Get-GuardRecords)
    Assert-Guards $guards
    $protectedPhysicalPaths = @($guards | ForEach-Object {
        Join-Path $generated $_.path.Substring($repository.Length + 1)
    })
    # Preflight the entire snapshot before deleting anything.
    foreach ($row in $plan.roms) {
        $null = Assert-RomPath $row.path
        $file = Get-Item -LiteralPath $row.path
        if ($file.Length -ne $row.bytes -or $file.LastWriteTimeUtc.Ticks -ne $row.writeTicks) {
            throw "ROM changed since the plan was made: $($row.path)"
        }
        if ($row.action -eq 'delete' -and
            ($file.Name -match '(?i)^clean\.nds$|baseline|accepted|rollback' -or
             $row.path -in $protectedPhysicalPaths -or
             $row.day -ge $plan.keepFromDay)) {
            throw "Protected/recent ROM in deletion list: $($row.path)"
        }
    }
    $keptHashes = @{}
    foreach ($row in @($plan.roms | Where-Object action -eq 'keep')) {
        $keptHashes[$row.path] = (Get-FileHash -LiteralPath $row.path -Algorithm SHA256).Hash
        $manifestPath = [IO.Path]::ChangeExtension($row.path, '.manifest.json')
        if (Test-Path -LiteralPath $manifestPath) {
            $manifest = Read-Json $manifestPath
            if ($manifest.candidate_sha256 -and
                $keptHashes[$row.path] -ine $manifest.candidate_sha256) {
                throw "Retained candidate does not match its manifest: $($row.path)"
            }
        }
    }
    $deleted = 0
    [long]$freed = 0
    foreach ($row in @($plan.roms | Where-Object action -eq 'delete')) {
        $full = Assert-RomPath $row.path
        $file = Get-Item -LiteralPath $full
        if ($file.Length -ne $row.bytes -or $file.LastWriteTimeUtc.Ticks -ne $row.writeTicks) {
            throw "ROM changed during cleanup: $full"
        }
        $hash = (Get-FileHash -LiteralPath $full -Algorithm SHA256).Hash
        [pscustomobject]@{event='before-delete';path=$full;sha256=$hash;bytes=$row.bytes} |
            ConvertTo-Json -Compress | Add-Content -LiteralPath $journalPath -Encoding utf8
        Remove-Item -LiteralPath $full
        [pscustomobject]@{event='deleted';path=$full} |
            ConvertTo-Json -Compress | Add-Content -LiteralPath $journalPath -Encoding utf8
        $deleted++
        $freed += $row.bytes
        if ($deleted % 100 -eq 0) { Write-Output "Removed $deleted ROMs ($([math]::Round($freed/1GB,2)) GiB)." }
    }
    foreach ($entry in $keptHashes.GetEnumerator()) {
        if ((Get-FileHash -LiteralPath $entry.Key -Algorithm SHA256).Hash -ne $entry.Value) {
            throw "Retained ROM changed: $($entry.Key)"
        }
    }
    Assert-Guards $guards
    $remaining = @(Get-Roms)
    $result = [pscustomobject]@{
        completedUtc=[DateTime]::UtcNow.ToString('o');plan=$planPath
        deletedRoms=$deleted;freedBytes=$freed;remainingRoms=$remaining.Count
        remainingBytes=($remaining | Measure-Object Length -Sum).Sum
        retainedHashes=$keptHashes;protectedSourcesVerified=$true
    }
    Write-Json $result $resultPath
    $result | Select-Object * -ExcludeProperty retainedHashes | ConvertTo-Json
    exit
}

$today = [TimeZoneInfo]::ConvertTimeFromUtc([DateTime]::UtcNow, $zone).Date
$keepFrom = $today.AddDays(1 - $KeepRecentDays).ToString('yyyy-MM-dd')
$guards = @(Get-GuardRecords)
Assert-Guards $guards
$protectedPhysicalPaths = @($guards | ForEach-Object {
    Join-Path $generated $_.path.Substring($repository.Length + 1)
})
$rows = @(foreach ($file in Get-Roms) {
    $full = Assert-RomPath $file.FullName
    $day = [TimeZoneInfo]::ConvertTimeFromUtc($file.LastWriteTimeUtc, $zone).ToString('yyyy-MM-dd')
    $reason = ''
    if ($day -ge $keepFrom) { $reason = 'recent' }
    if ($file.Name -match '(?i)^clean\.nds$|baseline|accepted|rollback') { $reason = 'protected-source-or-baseline' }
    if ($full -in $protectedPhysicalPaths) { $reason = 'protected-source-or-baseline' }
    [pscustomobject]@{
        path=$full;name=$file.Name;bytes=$file.Length;writeTicks=$file.LastWriteTimeUtc.Ticks
        day=$day;action='delete';reason=$reason
        hasManifest=(Test-Path -LiteralPath ([IO.Path]::ChangeExtension($full, '.manifest.json')))
    }
})
# Explicit pins support an older research dependency or a user-designated milestone.
$pinsPath = Join-Path $repository 'translations\rom_retention_pins.json'
if (Test-Path -LiteralPath $pinsPath) {
    foreach ($pin in @(Read-Json $pinsPath)) {
        $full = Assert-RomPath $pin.path
        $matches = @($rows | Where-Object path -eq $full)
        if ($matches.Count -ne 1) { throw "Pin is not in inventory: $full" }
        $matches[0].reason = 'pinned: ' + $pin.reason
    }
}
foreach ($group in @($rows | Where-Object day -lt $keepFrom | Group-Object day)) {
    # Prefer complete integrated candidates, then other manifested outputs.
    # Research-only days still receive historical checkpoints, without release credit.
    $pool = @($group.Group | Where-Object {
        $_.hasManifest -and $_.name -match '^all_routes_combined_v\d+_candidate\.nds$' -and
        $_.path.StartsWith($generated + '\out\', [StringComparison]::OrdinalIgnoreCase)
    })
    if (-not $pool.Count) { $pool = @($group.Group | Where-Object hasManifest) }
    if (-not $pool.Count) { $pool = @($group.Group | Where-Object { $_.path.StartsWith($generated + '\out\') }) }
    if (-not $pool.Count) { $pool = @($group.Group) }
    $ordered = @($pool | Sort-Object writeTicks,path)
    foreach ($checkpoint in @($ordered[0], $ordered[-1])) {
        if (-not $checkpoint.reason) { $checkpoint.reason = 'daily-checkpoint' }
    }
}
foreach ($row in $rows) { if ($row.reason) { $row.action = 'keep' } }
$remove = @($rows | Where-Object action -eq 'delete')
$stamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffffffZ')
$planPath = Join-Path $audit "$stamp.json"
$plan = [pscustomobject]@{
    format='dk4-rom-retention-v1';createdUtc=[DateTime]::UtcNow.ToString('o')
    storageRoot=$storage;timezone='America/Indianapolis';keepRecentDays=$KeepRecentDays
    keepFromDay=$keepFrom;roms=$rows
}
Write-Json $plan $planPath
[pscustomobject]@{
    plan=$planPath;keepFromDay=$keepFrom;totalRoms=$rows.Count
    keepRoms=@($rows | Where-Object action -eq 'keep').Count
    deleteRoms=$remove.Count;reclaimGiB=[math]::Round(($remove | Measure-Object bytes -Sum).Sum/1GB,2)
} | ConvertTo-Json
