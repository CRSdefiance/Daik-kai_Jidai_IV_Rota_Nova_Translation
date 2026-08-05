# Project to-do list

## High priority

- [ ] Develop the profile-driven English text system described in
  [text_rendering_roadmap.md](text_rendering_roadmap.md).
  - [ ] Phase 0: inventory renderer families and assemble a golden screenshot/record corpus.
  - [x] Phase 1: implement a lossless standard-dialogue tokenizer and hazard linter.
  - [ ] Phase 2: add extracted font metrics, pixel-width wrapping, and dialogue previews.
    - [x] Add deterministic profile-based pixel wrapping and line/page diagnostics.
    - [x] Add ILNK record/control inventories and diagnostic PNG previews.
    - [x] Keep all Phase 2 commands offline and non-ROM-mutating.
    - [x] Replace provisional base advances with traced game-font metrics (6 px ASCII,
      12 px Shift-JIS; 6-by-11 extracted ASCII glyphs).
    - [x] Cold-boot the 38/39-cell story boundary probe and measure runtime macro behavior.
    - [x] Calibrate and golden-test the 216-pixel/36-cell story window bound.
    - [x] Calibrate and golden-test the shared-message window bound (216 px / 36 cells).
    - [ ] Identify the live HELP.DK4 route, then calibrate and golden-test its window.
  - [ ] Phase 3: add a verified fixed-size encoder for `MESFILE`, `HELP`, and `SC0`–`SC3`.
  - [ ] Phase 4: map ILNK interior entry points and enable relocation only for proven blocks.
  - [ ] Phase 5: investigate a shared runtime Latin-renderer hook after the offline tooling is stable.
  - [ ] Phase 6: add adapters for ARM9 menus, compact HUD fields, packed tables, and graphics.
- [x] Map and translate the packed sound selector: 38 BGM titles and all 57
  fixed-slot or standalone SFX titles.
- [ ] Cold-boot `out/sound_selector_en_v3.nds`, scroll through all BGM and SFX
  entries, and confirm selection, playback, volume, and Back still work.
- [ ] Route the BGM selector through the normal narrow-Latin renderer so compact
  full-width labels can eventually be replaced by complete track names.
- [ ] Replace the Options Reports/Sailing Help full-width diagnostic text with release-quality
  narrow English after its renderer adapter is implemented.

## Release discipline

- [ ] Continue building every playable candidate directly from `out/all_goods_roundtrip.nds`.
- [ ] Require a source-locked manifest, regression verification, and cold-boot emulator test
  before promoting any candidate.
