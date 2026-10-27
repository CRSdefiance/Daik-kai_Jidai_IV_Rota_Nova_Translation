# Nagasaki signs and complete Shiraki surname V517–V518

## Normal Japan visit

Ordinary V514 cold-loaded the verified rested Seoul save. Normal sailing went
west clear of Korea's coast, then south and east to Nagasaki. Read-only original
terrain queries and actual ship snapshots guided corrections; no position,
supply, inventory or condition was injected. The real game offered **Dock at
Nagasaki?** at frame6440. Normal inputs entered town and resupplied.

The actual Japanese facility table selects the retained `kbj04` Tavern lantern
and `kbj08` Inn plaque. All923/1248 nontransparent pixels match their source
palettes at native color precision. Complete English glyph and blank-cell masks
match **Tavern** at (56,238)–(92,249) and **Inn** at (63,260)–(81,271).
These anchors differ from the older forced Lisbon fixture and are verified in
the real alternate town. The clear 酒 decoration and indistinct Inn plaque stay
unchanged, with their independent English facility labels providing the meaning.
No invented proper inn name or lettering is added.

Background47 matches all17,440 unobscured pixels in four town captures. Silver,
CotClth and T-Shell match every glyph and blank cell in all four captures. The
latter two are inherited abbreviations; this checkpoint does not rename them or
claim that the broader older-wording review is complete.

## Namahage dream and save

Entering the Inn naturally triggered Maria SC3 block171's Namahage dream. The
observed sequence uses an unseen FE voice on a black dream background, Yukihisa's
normal portrait, Angelo's response and the normal item-award display. It awarded
the **Namahage Cleaver** without an inventory fixture. This is not evidence that
the unidentified raw creature-introduction graphic was displayed; that gate
remains open. An additional paid Inn night ended at Mar12 with fatigue0.

Slot6 was saved on an isolated copy of the original Seoul cartridge file.
`E:/Rota Nova translations/Saves/maria-nagasaki-namahage-v514.dsv` is hash-pinned
in `work/analysis/japan_facilities_v517/saved_checkpoint.json`. The original Seoul
donor remains exact. The later ordinary V518 cold reload loads the Nagasaki game,
retains the whole upper town panel and visits both facilities again. Route
completion bits remain zero. Maria's initial user-authorized selection bypass
is part of the save provenance; it is not active in these runs or an earned unlock.

## Central surname correction

The portrait caption displayed **Yukihisa Shira**. RAM held that exact shortened
string, so this was a data error rather than missing letters in the renderer.
The clean eight-byte slot at ARM9 offset15BFD8 is
`83 56 83 89 83 4C 00 00`: **シラキ**, or **Shiraki**. The historical ASCII
profile had replaced it with `Shira\0\0\0`. The complete phonetic spelling
`Shiraki\0` fits the same slot. Only bytes15BFDD and15BFDE change; all other
bytes, pointers, neighboring fields, code and reserved pools remain exact.
The first NUL moves from slot byte5 to7, remaining inside the original extent.

This preserves the established surname already used in the character's story
introductions. The central provider supplies the complete spelling to its
consumers. Historical profiles retain their earlier bytes for reproduction;
the new registered late stage corrects the current release. The locked primary
names Rafael, Joakim, Maria and Camille are unchanged.

## Release evidence

- Seven actual dream frames match every glyph/blank cell of **Yukihisa Shiraki**:
  180 ink pixels, bounds(16,276)–(112,287), including the final **ki**.
- An exact-control replay compares31 shared frames. Changed pixels occur only
  in the portrait-nameplate band; all other picture, dialog and state pixels
  remain exact. The new nameplate remains within the native screen bounds.
- Six actual alternate facility cases across the original voyage, corrected
  dream replay and saved-game reload verify complete sprites and captions.
- All56 fresh title/New Game/story/town/Help frames match V514 exactly.
- All675 PXL/FLS files and every other ROM component remain byte-identical.
  All470 inherited batches and114 accepted layers remain. All921 graphics
  preservation entries are inherited by exact container equality.
- The clean-ROM xdelta reconstructs the candidate byte for byte.

Verifier: `scripts/verify_shiraki_japan_release_v518.py`.
Proof: `work/analysis/shiraki_surname_v518/release_proof.json`.
Targeted Ruff passes. These are targeted emulator tests, not a full playthrough
or physical hardware verification.

Candidate: `out/all_routes_combined_v518_candidate.nds`.
Profile: `all-routes-unified-v518`, experimental.
SHA-256: `c451a11bb696c71970d7224a5194e28ec57fa406995862f9cc8e0b67711173b7`.
Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
Only `/__arm9__.bin` differs from V514; there is no canonical promotion.

Osaka background37, Naha and the other recorded original gates remain open.
All22 original requirements and all18 incomplete plaques remain in the audit.
The graphics goal remains active. At its eventual completion, revisit older
record-based checks as requested.
