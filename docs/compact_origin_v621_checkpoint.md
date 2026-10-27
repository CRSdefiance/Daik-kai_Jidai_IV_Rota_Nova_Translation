# V620/V621: actual boarding duel and shared compact-text source origins

The preceding status-only turn made no authoritative implementation change. This
turn revalidated the saved V620 encounter and followed the next concrete action:
reproduce and repair its misplaced duel statistics. The full graphics goal remains
active. All18 original plaque/hint entries remain incomplete and all22 historical
requirement objects retain their exact scope.

## Actual V620 evidence and cause

V620 cold-boots unchanged V617 with the pinned Copenhagen donor. The new opt-in
battle fixture changes only own CMobileShip coordinates and, when needed, its
current hull/crew within the original observed valid48/19 state. It does not set
an encounter, victory, enemy stats, reward, inventory or artwork-selection flag.
Original terrain code verifies the nearby water point. At20400 the combined
recovery/proximity request moves own ship20 world units south of the original
Speyer fleet. Original subsequent simulation reaches a boarding duel by20800.

Both actual stat views select a shared464x96 source canvas. Their origins are
row24 and row36. V617's compact ASCII path selects the absolute single-character
callback020D501C without adding those view origins. Both actors therefore paint
at row0, overwriting the first name and leaving the intended stat panels empty.
The right name bar then clips the misdirected HP value. Apparent HP12/7 was not
evidence that the character was close to death: the complete underlying values
were124/73 in the displayed enemy stat string.

V157's earlier independent zero-origin raster tests and constructor/crop tests
did not combine the actual nonzero-origin view with this single-character path.
Their scoped passes do not clear the actual duel display. This is a concrete
older-evidence gap to retain for the eventual record-based completion review.

## Shared correction, with no new code allocation

The Market already uses a96-byte callback at01FFC71C that executes the original
view-origin getter, adds the local text point, and calls unchanged020D501C.
V621 reuses it for the shared bitmap-font callback atARM9 offset160400. The
callback's low byte1C preserves the existing compact class discriminator. The
Market's private callback already points there and remains unchanged. Controller
icon callbacks and paired CP932 callbacks remain unchanged.

Only one pointer changes:020D501C to01FFC71C, three differing bytes. No strings,
glyph rasterizer, font spacing, source crop, descriptor, image, palette, helper
code, section extent, startup/cache wrapper, staged pool or arena bound changes.
All other internal ROM files/components are exact V617. This corrects the shared
source-origin contract rather than moving the duel lettering by a screen offset.

Sixteen native replays cover both actors, old/new callbacks, their actual origins,
zero origins and supplied two-axis origins20/48 and300/72. The old path reproduces
row0 writes. Every new full canvas matches independent original-font masks and
retains all unowned rows. Zero-origin old/new canvases are byte-identical. These
supplied-origin controls are not additional gameplay screens.

## Integrated actual gameplay and regression

V621's full registered build contains470 batches and114 accepted layers. Both
emulator runs cold-boot with no savestate and end normally. Nineteen distinct
ordinary no-save/no-fixture New Game/Market frames match V617 exactly. The
preservation audit retains660 PXL headers/palettes/extents,261 FLS textures and57
embedded block extents. The clean-ROM patch reconstructs every candidate byte.

The duel run repeats the same source donor, input prefix and single proximity
fixture. At20800 and21200, both complete stat source rows match independent font
masks. All12 actual destination crops (Fencing, HP and Healthy for two actors in
two states) match the complete foreground/blank masks at original descriptor
destinations. A native refresh of both actors leaves all22272 canvas bytes exact
to the captured game. Both original name rows remain visible.

Normal subsequent inputs produce complete capture/victory notices at22400,
22800 and23200; all first/final letters, punctuation and blank cells pass source
font masks. Further observations show supplies,4617 seized coins,75 national
reward coins and Cargo Setup at24800. No victory/reward flag or enemy stats are
injected. This proves original outcome handling after the disclosed proximity
fixture, not normal long-distance travel or earned campaign progression.

Cargo Setup does not itself prove the Spoils/Distributed Goods headers or the
five miniature controls. Those remain open. The old Spever/Speyer spelling and
older awkward powder-fire wording remain source/editorial follow-ups. No whole
route or hardware verification is claimed.

## Artifacts and reproduction

- Candidate: `E:/Rota Nova translations/Generated/out/all_routes_combined_v621_candidate.nds`
- ROM SHA256: `dde6c124f790c6f9dff2cb606064ee3cd02944a70570f45b978f68c32a114ef2`
- ARM9 SHA256: `a49549b7300e6e101d52cdeabeab857ba32a20a49bbe7bad75f69d17a6f5be3b`
- Patch SHA256: `b4f3978e0560b99bed7b0af883c00db47f9151229cf2e133db35290722ecd343`
- Profile: `all-routes-unified-v621`; adjacent complete manifest required.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Source donor: `work/analysis/lubeck_voyage_v421/donor_test_copy.dsv`, SHA256
  `97997ce6fbeda9ff0272c08d7420e96676240b017e0037b721ed7c5eb52770d5`.
- Verifier: `scripts/verify_compact_origin_v621.py`.
- Native controls: `scripts/probe_compact_origin_v621.py`.
- Proofs: `work/analysis/compact_origin_v621/`.
- Full runs/native exports: `E:/Rota Nova translations/Generated/work/emulation_v193/compact_origin_v621_duel`
  and `compact_origin_v621_market`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V621 Compact source origins`.

Reproduce with `scripts/run_compact_origin_v621.py duel` in a fresh output folder
and PTY stdin, then replay the archived navigation journal through its normal
stop at24801. Use `market` for the separate no-fixture regression. Initial runner
attempts failed UTF-8 manifest decoding before emulator initialization; they have
no gameplay credit. An initial replay omitted actual captured ITCM and failed;
only the source/RAM/ITCM-bound replay above receives native execution credit.

Next continue the original post-capture Cargo Setup path with this proven input
schedule; inspect the real header selector/control consumers before declaring
Spoils or miniature graphics verified. Eight village cards, Confirm, remaining
legacy/comic/logo/movie/material contexts and broader gameplay remain open.
Canonical promotion and latest-verified pointers remain unchanged. Experimental
V621 is not a full-goal release. Older record-based checks remain due at actual
completion; user exemptions for the four low-resolution Online images and
preservation of the brown comic marks remain in force.
