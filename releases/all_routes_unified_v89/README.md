# Combined English patch: Unified V89

All four routes: Raphael V93, Hodram V32, Lil V123 and Maria V111, plus the
registered shared UI/text layers. Experimental candidate; emulator gameplay
verification and acceptance remain pending. Lil inventory: 6,539 translated,
69 native controls preserved, zero remaining records.

## Apply the patch

Use your own unmodified Japanese ROM with SHA-256
`f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.
Apply `translation.xdelta` with xdelta3 or the project tool:

```powershell
python -m dk4tool apply-xdelta path/to/clean.nds releases/all_routes_unified_v89/translation.xdelta --out out/all_routes_combined_v89_candidate.nds
```

Keep `release_manifest.json` beside the patch. The tool checks both the input
and reconstructed output hashes. No ROM is included in this repository.
The combined ROM is generated locally in `out/all_routes_combined_v89_candidate.nds`.

## Build and verification

Build with `python -m scripts.build_integrated_release --profile all-routes-unified-v89 --out out/all_routes_combined_v89_candidate.nds`.
The immutable build parent is `out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
The clean Japanese ROM above is the patch input, not the playable build parent.
All accepted layers remain baked into that parent. The profile applies 390
registered experimental batches. See `build_manifest.json` for the registry hash,
exact batch list, target checksum and changed records.

Exactly nine internal paths change relative to the accepted parent:
`/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`, `/__arm9__.bin`,
`/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`, and `/data/SC0.DK4` through
`/data/SC3.DK4`.

Verification includes baseline preservation, exact saved route records, packed
entry/formatting safety, and applying the patch to reconstruct the ROM byte for
byte. All 164 packaging, release-integrity, dialogue and Lil regression tests pass.
ROM SHA-256: `a727b361c9c3365acb8bcb7bea6f7debc42ef319eec1e7830742b1b32f85b580`.
Patch SHA-256: `73a4ee8bbb1de5a5447c3a566802e2c6241d79a45d8e6cef50ab69872f162a40`.
Four unsafe literal percentage signs in Lil's older market-share and ship
tutorials were rewritten in natural English and previewed before packaging.
See `exact_records.json`, `translation_integrity.json`, and
[translation progress](../../docs/translation_progress.md).

Cold-boot test the title menu, all captain selections and openings, town UI,
and representative story progression for each route. Test Lil's market-share
and ship tutorials and later exploration scenes. Do not load old emulator save
states for this verification. This package does not promote the canonical parent.
