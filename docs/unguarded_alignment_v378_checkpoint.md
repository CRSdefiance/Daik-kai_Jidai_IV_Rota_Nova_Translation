# Dialogue alignment checkpoint V378

Experimental combined candidate. The graphics goal remains active. All 22 historical
requirements and all 18 incomplete plaques/hints remain in the audit. The user's
exemption for low-resolution Online screenshots remains in effect.

## Fix and evidence

The sailing warning previously started its first row at x16 and its continuation at
x22. A scoped modal-painter helper now shifts an unguarded ASCII first row six pixels
when the next row has exactly two alignment spaces. It requires an initial pen,
zero tracking, and enough width for the native paired-glyph flush. Source text,
controls, macros, fonts, dimensions and continuation behavior are preserved.
Other inputs delegate to the inherited painter. Expanded runtime strings must pass
the same width check; stored-string coverage is not a claim about all substitutions.

- Seventeen native boundary/fallback cases verify complete pixels, input buffers,
  header fields, return values, stack and saved registers.
- A census of 369 matching records / 360 unique stored strings verifies the complete
  first-row shift and unchanged remaining pixels and returned pointer.
- The actual warning has both lines at x22, with 166 and 126 exact ink pixels.
  All changed pixels belong to the first row. Its continuation is unchanged.
- Final V378 passes 46 fleet/voyage, 34 sort, 23 New Game and 30 ordinary book
  purchase/equip frames. Fleet frames match the verified research result; other
  frames match V375 except the intended warning-row shift in the sort replay.
- All 470 inherited batches and every V375 stage remain. Only `/__arm9__.bin`
  changes from V375; graphics files, route/COMMON/HELP data and other components
  are byte-exact. Existing payload and SDK sections are preserved. The helper
  fits the existing 4096-byte allocation (3880 bytes used), without arena changes.
- The integrated builder, targeted Ruff, manifest/inheritance checks and exact
  clean-ROM patch reconstruction pass.

V376's earlier width-minus-six condition wrapped a near-full first row unexpectedly.
It is research only. V377/V378 reserve 18 pixels for the margin and native pair flush.
The census harness separately required non-overlapping context/buffer addresses and
a larger instruction allowance; those were test-harness corrections, not ROM fixes.

Evidence: `work/analysis/alignment_release_v378/release_proof.json` and the linked
native/census proofs. These are targeted cold-boot emulator tests without savestates,
not full route playthroughs or hardware tests. Older save history remains unknown.
Weapon/armor acquisition, alternate plaque states, retained environmental/legacy
consumers and deeper Gallery/endings remain open. Revisit older record-based checks
when the full goal is complete.

## Handoff

Candidate: `out/all_routes_combined_v378_candidate.nds`.
SHA-256: `46a66cfbd079a53dbb155d6a531eae6ac5d956fea93e4f3d9a5a8c679900620f`.

Patch: `out/all_routes_combined_v378_candidate.xdelta`.
SHA-256: `4cd4eb65152fb0fe988da07801e30e0bab625317992fa86895b7873171f38fe0`.
Patch input: `work/clean.nds`, SHA-256
`f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.

Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
Profile: `all-routes-unified-v378`. Accepted layers remain baked into the base;
all 470 inherited experimental batches and native stages are retained. Added stage:
`translations/unguarded_dialogue_alignment_v1.json`. The neighboring manifest lists
the complete layer identities and internal changes. Canonical promotion has not occurred.

Verifier: `scripts/verify_alignment_release_v378.py`, plus V377 native/census/live
proofs checked by the source-locked stage. User cold-boot areas: title/New Game,
established story/town, sailing warnings, Items > Equip, Info > Fleet Info,
Sailors > Sort and the ongoing Sailor Info/Assign Sailors variants.

The user-requested release destination is `E:\Rota Nova translations`; verified
guide captures are copied unchanged to its `Screenshots` subfolder. Repository
artifacts and reproducibility records are retained.
