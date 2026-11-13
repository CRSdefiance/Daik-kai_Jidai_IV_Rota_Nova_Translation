# V256 source audit: legacy maps and native seamap cache

V256 is research and audit reconciliation. **The playable candidate remains V255**:
`out/all_routes_combined_v255_candidate.nds`, SHA256
`9d8553cb2d1566a6754eb21269515e1af1677b51a4cce11450d4cdb92068ddc4`. No ROM, patch, release profile or production code changes.

## Corrected source classification

V194 had already established eight304x200 four-bit map paintings in
`/GRP/CMMNIMG.DK4` block3. V250 used32x32 and320-pixel partitions and mistakenly
reintroduced source-content uncertainty. Historical diagnostic outputs are retained;
their content classification is superseded by the revalidated V194 evidence.
The current source images are not a new discovery claimed from the repeated scan.

Current source row correlation independently favors304 pixels. The full source
243232-byte block consists of32 palette bytes and243200 packed pixel bytes.
Repacking is byte-exact. All eight60800-pixel cell hashes match V194 and every byte
matches canonical and currentV255. Eight full map paintings were reviewed without
cropping or downsampling. No separate Japanese caption or instruction is present;
retain the original cartographic artwork. No country/city names are inferred from
painted marks. This closes the false source-content uncertainty, not legacy runtime use.

## Native atlas source and load checks

The native `/_pxl/seamap.pxl` is an independently registered244x1280 four-bit atlas
with eight244x160 source pages, eight32-byte palette banks and pixel offset276.
Its whole source file remains exact to canonical. All64 page/palette color charts
were reviewed at source scale, with every saved pixel verified inside each sheet.
They contain map paintings without separate Japanese UI captions or instructions.
The source dimensions and palettes differ from the legacy block. Visual similarity
is not treated as byte-copy identity, native provenance or permission to resample.

Original resource registration runs at02010E190 and constructs owner02313B8C with
the actual `_pxl/seamap.pxl` filename. The original resource/cache/view code is exact
Japanese-ROM code. A bridge supplies only SDK filesystem open/read/seek/close against
the exact current ROM file. All handles close. Native code resolves the complete
header, every palette and every packed pixel byte, including guarded view writes,
stack and saved registers. Sixty-four native view cases pass: eight page origins
and eight bank IDs. The original constructor adopts244x160 extents and all supplied
source origins remain inside the declared atlas. No artificial image-header getter
or text renderer is substituted.

Page origins/extents and bank IDs are **supplied input contracts**. This does not
prove which game menu selects them, an actual GPU palette/alpha/UV choice, physical
filesystem behavior or how the legacy archive is used. No global unused-data claim
follows from missing fixed references. The unresolved native-storage count remains11.

## Artifacts and remaining work

- `scripts/research_map_sources_v256.py`: source assertions, native cache/view tests,
  exact view guards, saved-register/stack checks and complete chart bounds; Ruff passes.
- `work/analysis/common_paper_v256/proof.json`: revalidated source hashes,64 native
  cases and actual SDK bridge events, source decisions and verification limits.
- `legacy_and_native_maps_review.png`: every source pixel in the eight paired maps.
- `native_bank0_all8_source_pages.png` through bank7: every native page under each bank.

Both authoritative audits now distinguish source-content retention from unresolved
legacy/native use. All17 plaques plus Equipped Items and Armor/Weapon variants remain
**incomplete, pending continued audit**. Other native parents, Gallery/SLACK legacy
blocks, source transcripts for four Online bodies, naming consistency, occupied
items/health/mood states and full gameplay verification remain open. The graphics
goal stays active. Revisit older record-based checks at eventual completion.

Completed visual decisions are stored separately in work/analysis/common_paper_v256/native_source_visual_review.json. The native verifier revalidates its source and chart hashes on rerun, preserving the review without automatically claiming a new visual inspection.

