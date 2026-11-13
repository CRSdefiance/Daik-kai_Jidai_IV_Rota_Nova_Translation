# Generated ROM retention

Keep every generated ROM from today and the previous two calendar days in
America/Indianapolis. For each older day, keep the first and last integrated
candidate with a neighboring manifest. If none exists, use other manifested
outputs, then historical out-folder ROMs, then research ROMs. A day with only one
candidate keeps one checkpoint. Historical checkpoints do not imply acceptance,
successful testing, or release quality.

Days and first/last ordering use each ROM's filesystem last-write timestamp,
converted from UTC to Indianapolis time. This preserves the migrated archive's
original build timestamps rather than grouping everything by its migration day.

The canonical baseline, named accepted/rollback/baseline artifacts and files named
exactly clean.nds are additional protected exceptions. The original work/clean.nds
is outside the cleanup scope. The original clean source and registry-designated
baseline/rollback hashes are checked before and after cleanup.

Only .nds files in E:\Rota Nova translations\Generated and directly in
E:\Rota Nova translations are eligible. Patches, manifests, translation sources,
screenshots, emulator states, guides and all other research records stay in place.
Existing junctions are preserved. Old scripts and documents may reference a pruned
historical ROM: consult the retention journal and retained patch/manifest. Keeping
a patch does not by itself guarantee a particular research ROM can be reconstructed.

Run from the repository root after completed build/test work:

```powershell
# Preview only; writes a dated plan under work/rom_retention.
.\scripts\prune_generated_roms.ps1

# Apply the exact saved plan printed by the preview.
.\scripts\prune_generated_roms.ps1 -ApplyPlan 'C:\...\work\rom_retention\<timestamp>.json'
```

The script defaults to three recent days; use -KeepRecentDays to change this when
planning. It refuses changed ROMs, paths outside the approved physical folders,
links, recent-file deletion, and reapplying a started plan. It records a SHA-256
before each deletion and checks every retained ROM's hash afterward. Deletions are
permanent; the JSONL journal is an inventory, not a backup. An interrupted run
retains its journal; inspect it and generate a fresh plan to continue.

For a research dependency or user-designated milestone that must stay longer,
create translations/rom_retention_pins.json before planning:

```json
[
  {
    "path": "E:/Rota Nova translations/Generated/out/example.nds",
    "reason": "Required input for ongoing research"
  }
]
```

Pins are explicit exceptions to the daily cap. Pin missing/changed dependencies
before cleanup, and remove stale pins when that work is complete. Retention runs
are manual; no scheduled job or build-time deletion hook is installed.
