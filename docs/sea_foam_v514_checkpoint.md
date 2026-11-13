# V514 sea-foam dialogue repair

## What changed

A normal Hodram voyage on V508 exposed an incomplete reaction (`The rumored... G`)
and generic warnings that omitted the original danger: the foam can swallow ships.
The complete original family, COMMON messages 457–480, is now reviewed against
the clean Japanese source and written as natural English paragraphs. Packed
records contain complete independent messages. Literal I/F characters use the
existing control-safe encoding; the manuscript contains ordinary English.

The first prototype passed supplied direct-parent tests but its actual captain
order split **to** across lines. Those tests did not cover the real sea callers.
An additional crew-table gate repaired the crew pages but still missed the captain.
Neither preliminary prototype was published. The final repair covers the original
queued crew parent 02053DB8, captain-table parent 02053C14 and captain numerical
parent 02053C5C, scoped to this family and the four original voice tables. It uses
the existing paragraph formatter, without manually authored line breaks or
shortening dialogue to fit the old allocation. Other dispatches remain unchanged.

COMMON cache block lengths, NUL counts, the directory and all 3,668 message
identities remain intact. Only necessary native offsets change. The dispatch uses
owned ITCM padding, verified as zero in two parent-ROM runtime exports. No section,
heap, cache, pool or persistent allocation grows.

## Evidence

- `work/analysis/sea_foam_family_v514/native_proof.json`: all 24 complete variants,
  52 cold/warm copies including neighbors, 7,336 direct-parent destinations,
  queued numeric dispatches and adjacent voice-table addresses. All source and
  destination guards, complete glyph sequences and whole-word rows pass.
- `work/emulation_v193/sea_foam_family_v514_final_actual/capture_report.json`:
  a cold boot with the copied genuine Ceuta cartridge save and the same normal
  input schedule as the original voyage. No savestate or movement injection.
- `work/analysis/sea_foam_family_v514/release_proof.json`: five actual pages
  (457, 463, 469, 470, 478) match every glyph and blank cell. Both line origins
  are x22; changed pixels stay inside the dialogue body. The evacuation order
  retains **to** as a whole word. All 56 fresh-game title, New Game, story, town
  and Help captures match V508 exactly. Resident repair code is exact after both
  runs. The clean-ROM xdelta reconstructs the candidate byte for byte.

## Registered candidate and limits

`out/all_routes_combined_v514_candidate.nds`, profile `all-routes-unified-v514`.
SHA-256: `c1416987c757f16c32f90e36c5f31db3f02529f6ceccf8b78cd3b0127f885199`.

The canonical base is `out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
All 470 inherited batches and 114 accepted layers remain. Only ARM9 and
`/COMMON/MESFILE.DK4` differ from V508; all 675 PXL/FLS files and other components
are byte-identical. The 921-entry graphics preservation ledger is inherited by
exact container equality.

Experimental; human acceptance and physical hardware testing are not claimed.
Actual replay covers five selected voices, while the other 19 variants have
native checks. This does not establish every dialogue context throughout the game.
All 22 original graphics requirements and all 18 incomplete plaque entries remain
in the audit. The graphics goal is active. At its eventual completion, revisit
older record-based checks as requested.
