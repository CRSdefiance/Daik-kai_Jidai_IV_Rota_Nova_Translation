# Project to-do list

## High priority

- [ ] Develop the profile-driven English text system described in
  [text_rendering_roadmap.md](text_rendering_roadmap.md).
  - [ ] Phase 0: inventory renderer families and assemble a golden screenshot/record corpus.
  - [ ] Phase 1: implement a lossless standard-dialogue tokenizer and hazard linter.
  - [ ] Phase 2: add extracted font metrics, pixel-width wrapping, and dialogue previews.
  - [ ] Phase 3: add a verified fixed-size encoder for `MESFILE`, `HELP`, and `SC0`–`SC3`.
  - [ ] Phase 4: map ILNK interior entry points and enable relocation only for proven blocks.
  - [ ] Phase 5: investigate a shared runtime Latin-renderer hook after the offline tooling is stable.
  - [ ] Phase 6: add adapters for ARM9 menus, compact HUD fields, packed tables, and graphics.
- [ ] Map the packed BGM/SFX selector strings and their interior pointers before translating them.
- [ ] Replace the Options Reports/Sailing Help full-width diagnostic text with release-quality
  narrow English after its renderer adapter is implemented.

## Release discipline

- [ ] Continue building every playable candidate directly from `out/all_goods_roundtrip.nds`.
- [ ] Require a source-locked manifest, regression verification, and cold-boot emulator test
  before promoting any candidate.
