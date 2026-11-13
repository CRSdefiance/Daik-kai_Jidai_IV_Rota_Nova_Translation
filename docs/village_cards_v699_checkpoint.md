# V699: eight village cards through the original event-image renderer

## What this closes

All eight translated white village-caption cards now have full actual emulator
display checks through the original event-image parent, loader and renderer.
This is a new fixture-based display result, not a discovered ordinary village
trigger. The source cards remain in place and unchanged.

V427/V589 found no direct story encoding for these cards; V426 excluded them from
all original Gallery image lists. V656 classified the remaining WorldMap byte
matches as compressed terrain input. Those negative source results are retained;
this checkpoint does not repeat them or infer global non-use.

## Declared fixture

Nine complete 4,000-frame V692 cold boots use the existing authorized system-unlock
donor and original Maria New Game inputs. The original script requests image 84
at frame 3749 through `02028AA8`, with caller return `02029FB8` and scene object
`02276F88`. Eight isolated runs replace only the incoming ARM9 R1 value with
168,169,170,171,206,207,208 or209. A disabled control keeps image84.

The actual source instruction and all three scene-option words are checked from
the captured original script/stack. The options live in DTCM; they are not assumed
to be a supplied synthetic mode. Original parent code is identical in clean and
current ROMs. No ROM, story instruction, source picture, save, WRAM, DTCM, ITCM,
flag, quest state or route progression is replaced by this fixture.

Full before/after CPU bytes prove exactly one changed byte at offset20, within
R1. Every other CPU byte and all 4 MiB WRAM,16 KiB DTCM and32 KiB ITCM remain
exact at the intervention. Each run applies once. All host hooks are restored and
the core DLL stays exact. This argument is consumed by the original function;
there is no persistent lookup/flag to restore.

## Verification

- All eight cards have two complete opaque holds at frames3900/4000:
  16 whole256x192 planes, **786,432 native five-bit RGB pixels**, source-exact.
- The disabled control's original image84 also matches two complete source
  planes:98,304 pixels.
- Every held snapshot contains exactly one complete byte-exact resident PXL for
  its requested image. No substitute loader, pixel injection or SDK bridge runs.
- All96 complete pre-fixture two-screen RGB and4 MiB RAM pairs match the disabled
  control. All eight full callback-entry CPU/WRAM/DTCM/ITCM states match it too.
- All16 lower-screen held images match the disabled control completely.
- Five native host-prefix/ABI controls and eight bounded-read controls pass.
  Thirty-seven fixture-plan controls cover each card's selected,disabled,already
  applied and other-image behavior, plus invalid word,PC,scene,LR and option pointer.
- All eight current PXL files remain byte-exact to the reviewed V414 versions.
  Complete photo comparison includes the image207 upper source stroke, all leading
  and trailing letters, every background cell and all display boundaries.

An initial pilot rejected an option pointer because its guard incorrectly allowed
only main RAM. No fixture was applied. The complete terminal run, failed guard
receipt, source and initial preflight are retained. The corrected producer accepts
bounded DTCM and validates options against the actual original instruction. It
remains frozen across all nine final runs.

## Visual/source review

Both the eight complete two-screen captures and the original-Japanese versus
actual-English comparison sheet were opened. The source pictures themselves are
white fields with handwritten regional/development labels; no village landscape
has disappeared in translation. The English labels preserve those meanings:

| Image | English |
|---|---|
|168|Arab Village 1|
|169|New World Village|
|170|Chinese Village|
|171|North Sea Village|
|206|Arab Village (Developed)|
|207|New World Village (Developed)|
|208|Chinese Island (Developed)|
|209|North Sea Village (Developed)|

All captions fit without missing first/final characters. The original clipped
stroke at the top of207 is retained exactly; its identity remains unresolved.
These are diagnostic fixtures and must not be promoted to the guide or described
as normal village arrivals. Ordinary scene reachability and indirect/generated
consumers remain open, despite this stronger native display coverage.

## Release and evidence

The production ROM remains `out/all_routes_combined_v692_candidate.nds`, SHA256
`0ff197ce9bbb48898c74a3c664609196867a5662bc3b346c612709038c54a47e`.
No V699 ROM, artwork edit, registry update, patch change, canonical promotion,
commit or push is created.

Analysis is in `work/analysis/village_cards_v699/`; final proof is in
`final/proof.json`. Captures remain under
`E:/Rota Nova translations/Generated/work/emulation_v193/village_cards_v699_*`.
The checked archive is
`E:/Rota Nova translations/Screenshots/Test fixtures/V699 Village card displays`.

All18 original plaque/hint entries stay incomplete, all22 historical requirement
objects stay preserved, and the full graphics goal remains active. Other controls,
comic playback, legacy/embedded contexts, texture/restoration review, older record
checks and final acceptance remain open. V698's code-prefix failure and V694's
separate suffix-memory differences are not cleared by these card results.
