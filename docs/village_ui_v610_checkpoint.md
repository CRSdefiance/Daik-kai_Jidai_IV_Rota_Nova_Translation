# V610: all village names/menu labels and actual password/developed-port path

V608 made progress by correcting village portrait wrapping. This batch completes
the 24 village name descriptors and six menu captions in English, reconciles the
three existing Leveque story references, and reaches an actual developed village.
It also catches and rejects a new startup regression before handoff. The full
graphics goal remains active.

## Registered build

- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Experimental profile `all-routes-unified-v610`: all 470 inherited V608 batches
  and all 114 accepted layers, named individually in the adjacent manifest.
- Candidate: `out/all_routes_combined_v610_candidate.nds`, physically
  `E:/Rota Nova translations/Generated/out/all_routes_combined_v610_candidate.nds`,
  SHA256 `bf3dbc0cf6e27c73f08d2e12c7f91ce0ee9bbe180e0cd01d6248983aa8f67599`.
- Exact clean-ROM `.xdelta` SHA256:
  `43b97163853f12cdc62d5f2d26f7471f49dfce753d7364ad1f07df8552146db8`.
- Only `/__arm9__.bin` and `/data/SC2.DK4` differ from V608. Every graphics file,
  COMMON archive, other route and component remains byte-identical to V608.
- Experimental; no user/physical-device acceptance or canonical promotion.

Wording and place-name rationale are in
[Village name decisions](village_names_v610_decisions.md) and the reviewed
natural-dialogue-v2 term manuscript `translations/village_ui_manuscript_v1.json`.
The six original action IDs, order, callbacks and unlock rules remain intact.
The only story edit is Lebaque -> Leveque in three Lil records. Both names are
seven bytes; every preamble, control byte, line break, other prose byte, record
length, block length and byte parity is preserved. This is not a new translation
or approval of those older paragraphs. Their broader prose review remains due.

## V609 rejected; storage isolation

The first registered candidate V609, SHA256
`8a5d32954b482cfd47e91408964a3d200c0023f5ae57087b9cb1cb72124a68a2`,
added 320 bytes to late-copy storage. The unchanged Syracuse schedule and a
separate 24,100-frame ordinary New Game/Market schedule both remained at a black
upper screen with Press START below. A separate late-START test also failed to
advance. No callback errors did not make this a boot pass. The coordinate helper
correctly refused to write without an active ship. V609 is rejected, not a parent
or user handoff. Its initialized English name getters receive no display credit.

Two explicitly labeled research ROMs were tested with the same donor and inputs:

1. Restoring all 30 original pointers and original SC2 while retaining the larger
   storage layout still reproduced the startup failure.
2. Keeping all 30 identical English labels and the three story-name corrections
   within existing storage reached sailing normally. Its complete frame 5200
   reproduces the registered V610 scene.

This isolates the failure from the English wording and route-name edits to the
larger storage layout. It does not establish the deeper scheduling/cache/memory
mechanism. Future expansion beyond the tested V608 late-pool extent remains a
specific unresolved risk requiring new source-bound boot evidence.

## Compact source ownership

V610 preserves all staged sections, startup calls, heap/arena bounds, cache and
autoload bytes exactly to V608. No native rendering/input/resource code changes.
An exhaustive byte-position census confirms each of the 30 original text owners.
The English strings use three exclusively owned source-name text spans:
15ADF8-15AE84,15AE90-15AECC,15AED8-15AF1C, 268 bytes total. Four-byte-aligned packing
fills those spans without shortening any English label.

An initial contiguous-pool guard correctly rejected nonzero unowned metadata.
The interleaved `8CVillage` RTTI name and three-word type-info record are preserved
in full. Stay fits its own five-byte source slot. Hekla and Promised Words reuse
their existing immutable English answer/title strings. No storage or runtime hook
is added. Every other main-section byte is verified exact after restoring only
the owned text spans and pointer fields.

## Actual 14,200-frame village run

The source Syracuse donor remains SHA256
`958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb`.
Cold boot uses an isolated copy and no savestate. The source-checked Inuvik water
fixture owns eight ship-coordinate bytes, with six actual changes. No discovery,
development, dialogue, resource, inventory, health or money flags are supplied.

- Discovery and docking show complete `Discovered Inuvik.` and `Dock at Inuvik?`
  masks, including the initial I and final punctuation.
- All six English menu captions pass 36 complete masks across six input states:
  4,164 ink pixels and every foreground position in six complete 96x120 regions.
  The menu's native foreground is RGB(8,8,8), distinct from the dialogue palette.
- The actual initialized models and virtual name getters return all 24 complete
  names. Every non-name model byte/geometry remains equal to V608. All 24 names
  also execute the original Common297 getter/variadic discovery formatter to both
  exact complete buffers. Interactive drawing is the explicit stopping boundary
  of those CPU preparation cases; they are not 24 ordinary village screenshots.
- The ordinary keyboard enters Aurora through 18 observed controller/stylus
  steps. Focus is inspected between actions, avoiding V607's mistaken repeated
  default-letter selections. Actual RAM independently confirms all observed
  prefixes, final `Aurora`, cursor 6 and capacity 18. No text is injected.
- The original case-sensitive password branch accepts it. The source-identical
  success code changes the original town90 development check from 0 to 2.
- Frame 11300 displays the translated stairway-to-heaven clue. Frame 11700
  displays the complete three-row next-visit facilities message. The source game
  removes the now-unneeded password menu option.
- Set Sail executes the original departure/payment flow. The subsequent original
  Dock prompt and Yes selection reach developed Inuvik at frame 14200, with its
  English header and facilities. No second location fixture is needed.

These are genuine original input/acceptance/development operations inside an
isolated location fixture. They do not claim ordinary long-distance travel,
progress in the user's save, all 24 developed villages or physical hardware.
No white village-card graphic is credited from this sequence.

## Regression, preservation and artifacts

A separate 24,100-frame ordinary New Game/Market run has no existing save or
synthetic fixture. All 19 sampled complete frames match V608 exactly. The full
registered builder/manifest, deterministic two-file transform and exact clean-ROM
patch reconstruction pass. Fresh checks retain all 660 PXL headers/indexed
palette banks/extents, 261 FLS textures and 57 embedded block extents.

`work/analysis/village_ui_v610` holds the transform, release, preservation,
keyboard-navigation and final input evidence. The predecessor research controls
and rejected reports remain under `work/analysis/village_ui_v609` and E's native
capture directories. Reproduce the final candidate only through
`build_integrated_release.py --profile all-routes-unified-v610`; research ROMs are
not distribution files. `verify_village_ui_v610.py` verifies all named evidence.

Selected unmodified village captures, rejected/control captures, scripts and
provenance are saved under E's `Screenshots/Test fixtures/V610 Village UI`.
Ordinary Market guide candidates are separate; publication is unapproved.

The observed Japanese village-name/menu gap is corrected, and V608's request wrap
remains fixed. The deeper larger-pool failure mechanism, other village contexts,
eight original village-card contexts, other legacy/comic/material/movie gates and
broader gameplay acceptance remain open. All 18 plaque/hint objects remain
incomplete, all 22 historical requirement objects retain their exact scope, and
older record-based checks remain a follow-up at full goal completion.
