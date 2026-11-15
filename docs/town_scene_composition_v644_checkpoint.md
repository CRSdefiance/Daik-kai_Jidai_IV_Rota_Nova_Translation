# V644: complete current Town composition with captured VRAM and DTCM

## Result

The original Town drawing iterator and shared-footer call rebuild both complete
Narvik screens exactly after poisoning all196,608 destination bytes. All98,304
output words match physical VRAM including bit15. Expanding those original words
through the capture's RGB565 conversion also matches every RGB888 screenshot
pixel, with no excluded border, text, icon, material or background region.

This resolves the missing-memory dependency retained by V643 for its observed
Town state. It uses V643's actual current V640 capture at15700, not a new emulator
run. The original source was a fresh cold boot with only the disclosed ship-location
fixture; Narvik development was produced by normal keyboard acceptance. No full
route, earned long-distance travel or hardware claim is added.

V640 remains SHA256
`93868a0b250a3b52897225dac48ab29e0b14d1f097208ca9a418208dd29d0b9e`.
No ROM, patch, source art, font, wording, registry or release pointer changes.
The prior V643 turn made progress on original village background selection and
the complete native backdrop. The full graphics goal remains active.

## Actual memory mappings

The read-only native export supplies main RAM,16KiB DTCM,32KiB ITCM, register
bytes and physical LCDC memory. All recorded files and their enclosing report
are hash checked. Serialization matched same-frame direct main RAM and left it
unchanged; no state is loaded.

Captured bank registers A-I are83,8B,84,81,82,00,83,00,82. The bounded mapper follows
the pinned core's bank purposes, physical16KiB pages, refresh order and documented
CPU-window mirrors. It accepts only this source-reviewed configuration; other
configurations are rejected. CPU-unmapped pages remain unmapped, rather than
receiving guessed zero data. Texture-only banks are not treated as CPU pixels.

The original5688 VRAM reads select logical0601BFC8..0601DFCC, mapped to physical
LCDC07BFC8..07DFCC in bank D's off-screen glyph cache. None overlaps either visible
framebuffer. No replay write targets VRAM, so byte-exact alias copies do not need
write synchronization in this test. Both actual ITCM aliases are restored, and
every fetched instruction word matches captured main RAM or ITCM.

Primary implementation: the existing pinned DeSmuME source at commit
95b4d798731caa809125b6c3c11d17cc332ff6ef, `MMU.cpp` bank mapping/mirror code and
`MMU.h` page constants. Both source files are hash-bound in preflight; MMU.cpp
also matches the earlier official source receipt. This is a bounded mapping of
the observed state, not a generic DS memory or hardware-timing implementation.

## Original traversal and complete output

The original source fragment020D32B8..020D3314 starts from the captured Town
renderer023117AC. It follows original next links, applies original enabled and
virtual visibility checks, invokes17 painters from18 registered nodes, and then
executes the original shared footer020CA668. The one hidden node remains hidden;
no callback is forced on or reordered to match the image.

Destination surfaces022E1794(lower) and022F9794(upper) are completely poisoned first.
Original stores assign every pixel. Adjacent guards, caller stack and preserved
registers pass. The surrounding SDK/GPU frame setup and submission timing are
outside this replay; no loader, getter, glyph or painter bridge is substituted.
The captured code and resources remain unchanged.

Erasing both captured visible VRAM outputs before replay produces exactly the
same rebuilt surfaces. Together with the complete VRAM-read trace, this rejects
circular use of finished screen pixels as an expected source. Prior source-file,
English wording and independent font audits remain separate evidence; exact
composition is not used to infer translation fidelity in every other context.

## Shared footer: source, final letters and failed models retained

The Town iterator alone leaves1600 differing footer pixels. The original footer
call reduces that to140 missing Menu/Select strokes. Its real bitmap header is
022CF7DC; its source pixels point to027E0000 in DTCM. Loading only compiled initial
DTCM data leaves these pixels blank. Restoring the actual captured DTCM resolves
all140 differences without any production change.

The actual source pointers name `Menu` and `Select`. Original metadata selects
24/36-pixel widths and source origins36/0. An independent original-font mask
verifies all720 active cached cells,140 foreground points and every blank cell.
The inactive cache tail contains172 nonzero cells retained from other labels;
original inactive metadata never draws them. The initial whole-cache-zero-tail
assumption was rejected; no cached source bytes are erased in the positive test.

Four source-cell deletion controls reject missing Select's first S/final t and
Menu's first M/final u. They cause exactly15,12,29 and13 differing visible pixels
respectively; every other pixel stays exact. An absent-footer-DTCM control
reproduces exactly140 missing strokes. These corruptions occur only in isolated
negative-control memory, never in the ROM, real emulator or save.

## Artifacts, visual review and remaining work

- Verifier: `scripts/verify_town_scene_v644.py`.
- Bounded mapper/diagnostics: `scripts/research_town_scene_v644.py`.
- Proof and native16-bit output: `work/analysis/town_scene_composition_v644/`.
- `complete_both_screens_NATIVE_REPLAY_RGB8.png` is an exact-color derivative.
  It was visually reviewed at native scale; the original capture remains separate.
- Earlier missing-VRAM, no-footer and missing-DTCM diagnostics/scripts are retained.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V644 Complete Town composition`.
  One explicitly reused, unmodified V643 screenshot accompanies the reconstruction.
  No additional guide candidate or newly captured gameplay is claimed.

All18 original plaque/hint objects remain incomplete, and all22 historical
requirement objects/scopes remain unchanged. Other scenes/states, miniature/Confirm
parents, white village-card contexts, raw comics, sepia/legacy maps, standalone
title consumers, other movie/material variants, wood-texture acceptance and final
candidate acceptance remain open. Low-resolution Online exemptions and brown-mark
retention remain. Older record-based checks remain due at full-goal completion.
