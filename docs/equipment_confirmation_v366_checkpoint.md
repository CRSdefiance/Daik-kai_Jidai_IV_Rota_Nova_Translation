# Equipment confirmation checkpoint V366

Status: experimental combined candidate. Full graphics goal remains active and
incomplete; canonical baseline is unchanged. All18 plaques/hints and their
remaining equipment, condition, fleet and route variants remain incomplete.
Low-resolution Online screenshots remain exempt under the user's instruction.

## Fix and source review

Two native COMMON messages,321 and327, contain the same Japanese confirmation:
`%sが\n%sを装備しました`. Their existing English `%s equipped %s.` correctly
preserves the completed action, actor and item. No translation, names, controls,
script metadata or record allocation was changed.

The scoped formatter wraps expanded equipment confirmations at spaces. It applies
only to these two message IDs through native parent return020546E8. Other paths
tail-call the inherited wrapper, including its existing tribute-message behavior.
The first-row budget reserves room for the existing initial alignment helper;
continuations retain the ordinary two-space machine guards. Previously declared
ITCM allocation, all earlier payload bytes and heap/arena bounds are preserved.

The actual Guild purchase/Items/Y Equip path uses321. V363 and its V364 long-item
replay incorrectly targeted only327 and still split `Ma / rco`; they are research
artifacts, unregistered and unsuitable for handoff. A native trace of the real
varargs caller, COMMON lookup, sprintf, macro expansion and wrapper verifies both
IDs in V365/V366. The obsolete fresh-game V308 timing also failed to reach the
intended current equipment scene; it receives no confirmation credit.

## Verification

- All198 native item getter names with five locked captain names:990 expansions,
  1980 native pixel cases, intact words/first/final letters and full font pixels.
  This census includes names that are not all equippable or normally available.
- Forty native boundary cases for the unguarded327 duplicate retain complete
  letters and whole words. Both native caller paths and unrelated-message scope
  checks pass. Actual gameplay credit is specifically the ordinary321 path.
- Actual ordinary cartridge-save purchase/equip of Travels of Marco Polo shows
  the complete confirmation, with478 native lettering pixels and final blank
  cells exact. The measured paper composition contract is origin(16,296), with
  16-pixel displayed row advance; the isolated glyph context advances12 source
  pixels. Physical composition is an actual-screen contract, not an independent
  whole-GPU trace. Every tested expansion fits the48-pixel displayed height.
- All22 captured short-equipment replay frames remain byte-exact. The long-name
  correction changes only182 screen pixels inside the confirmation text bounds;
  the rest of the actual final frame is exact.
- Registered V366 cold boots normally: all23 New Game frames match the previous
  production replay; all30 ordinary purchase/equip frames match verified V365.
- All470 inherited batches and every V360 native stage remain present. Only
  `/__arm9__.bin` differs from V360. Every route, COMMON file, PXL/FLS graphic and
  other ROM component is byte-identical. Earlier ARM9 sections/payload/code are
  restored byte-exact by the guarded stage's preservation checks.
- Integrated builder, targeted Ruff checks, saved-ROM/manifest checks and exact
  clean-ROM patch reconstruction pass.

These are targeted cold-boot DeSmuME checks, not complete route playthroughs or
physical-device tests. Weapon/armor occupancy, alternate health/moods, deeper
Gallery/ending contexts, retained environmental/legacy graphics consumers and
the other historical audit requirements remain open. Revisit older record-based
checks when the full goal is actually complete.

## Handoff

Candidate: `out/all_routes_combined_v366_candidate.nds`.
SHA-256: `53a789aebc783be47b1cf8991e823f9ee4ae6d26324dfeb884f7ec6402de6381`.

Patch: `out/all_routes_combined_v366_candidate.xdelta`.
SHA-256: `3ee0273823151b92799d4774c3672b020c8df5470c83b9a62e643ab2f08a168f`.
Patch input: `work/clean.nds`, SHA-256
`f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.

Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
Profile: `all-routes-unified-v366`. Accepted layers remain baked into the base;
all470 inherited experimental batches/stages are retained. Added experimental
stage: `translations/equipment_confirmation_wrap_v1.json`.
Complete layer identities, internal changes and checks are in the neighboring
`out/all_routes_combined_v366_candidate.manifest.json`.

User cold-boot areas: title/New Game, town and established dialogue, Items >
Equip with short and long item names, and ongoing Sailor Info/Assign Sailors
variants. Candidate remains experimental; explicit user acceptance is required
before canonical promotion.

Evidence and verifiers:

- `work/analysis/equipment_wrap_v365/`: native scope/caller, pixels, boundaries,
  source review and research plan.
- `work/analysis/equipment_release_v366/`: actual glyph/change bounds and final
  release/patch evidence.
- `scripts/verify_equipment_wrap_scope_v365.py`
- `scripts/trace_equipment_wrap_v365.py`
- `scripts/verify_equipment_wrap_pixels_v365.py`
- `scripts/verify_equipment_unguarded_v365.py`
- `scripts/verify_equipment_live_v365.py`
- `scripts/verify_equipment_release_v366.py`
