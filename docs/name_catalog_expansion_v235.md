# V234 complete prose: catalog expansion V235

V235 is source-locked ARM9 research, not a ROM candidate. V218 remains unchanged
and the full graphics goal active/incomplete. The previous turn reviewed30 fresh
SC0 lines;15 needed private allocation to retain their complete meaning.

## Implemented and verified

The combined catalog now covers **50 records**:25 original capacity cases,10 V232
corrections and15 V234 corrections. It contains **81 unique NUL-inclusive keys**.
All original selected source/target pairs are retained; the combined table/helper
is rebuilt from the exact V218 source rather than chaining research hooks or
moving script records. The original three caller scopes remain unchanged.

All **128,492 route segments** are audited. Only the50 reviewed source owners match;
every selected owner is covered and no extra/unreviewed match is accepted. Duplicate
new owners or same-key conflicting translations fail preparation. All SC0–SC3
resource bytes and command/record boundaries stay intact.

Native verification passes:

- **1,296 lookup cases:**81 keys, four source alignments, three scoped callers plus
  a foreign caller, with original arguments/registers/stack/source guards intact.
- **243 altered-input rejections:** extra bytes before the NUL, truncation and
  changed first bytes do not accidentally select a complete-key translation.
- **243 complete native copies:** all81 keys through all three callers preserve
  full output, beginning/end bytes, controls, name expansions, NUL and guards.
  The company-name FO expansion now has explicit coverage alongside FI/FA/FU.
  No getter or macro-result bridge supplies expected output.
- Actual late-copy startup/cache and ARM7 ownership pass. All **52,576 inherited
  pool bytes**, other original sections and the original expander remain exact.
  The new **61,248-byte** payload fits its explicitly bounded pool/staging spans.

The generic preparation/verifier CLIs accept explicit research paths/counts, while
retaining the original V233 defaults and exact V218/hash/name/caller/source gates.
Existing V233 results are not overwritten. Ruff passes.

## Scope and remaining gates

The real player fixture remains the explicitly identified V201 named research
cold-boot RAM. Its ROM/capture/RAM hashes and static-difference ownership are checked.
This is full native expansion evidence, not a changed V218 physical playthrough or
proof of every original scene's portrait, timing, crop or transition.

The fifteen corrected sentences are not shortened for capacity. The other fifteen
fixed-slot V234 lines remain outside the playable ROM, as do the nine fixed-slot
V232 lines and the remaining name migration. No partial five-name-field patch or
catalog binary is registered/distributed as a playable candidate.

Full integration still requires the remaining source/editorial/layout review,
complete macro/profile updates, current-source registration, combined ROM/patch
and representative physical scene checks. Four Online bodies, ambiguous source
marks and other graphics/native/contextual/gameplay scope remain open. Keep the
requested older-record-check follow-up for eventual completion.

## Evidence and reproduction

`work/analysis/name_catalog_v235/` contains `catalog_plan.json`, `route_scope.json`,
`catalog_research_arm9.bin` and `native_proof.json`. The V234 source manuscript and
reviewed full previews remain the editorial input.

```text
python scripts/prepare_name_catalog_v233.py --out work/analysis/name_catalog_v235 --prior-plan work/analysis/name_catalog_v233/catalog_plan.json --expected-inherited 35 --formatting-report work/analysis/name_editorial_v234/formatting_report.json --manuscript translations/confirmed_name_route_editorial_v234.json --expected-additions 15
python scripts/verify_name_catalog_v233.py --root work/analysis/name_catalog_v235
```

These commands produce/check research bytes only. They are not a playable-ROM
build path. Registered V218 remains SHA-256
`be05e432cda1b32c18f6b1fbca8c57d6069a442ea87c2c158388fe38f3d5220f`.
