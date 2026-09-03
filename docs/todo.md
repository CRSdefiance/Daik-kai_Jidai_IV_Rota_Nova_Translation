# Project to-do list

## High priority

- [x] Correct route ownership: SC1 is Hodram's playable route; SC2 is Lil's. Revoke
  the inaccessible wrong-route SC2 control probe and retain its ROM only as evidence.
- [x] Translate 67 records from Hodram's actual SC1 opening through the first
  Lil/Kamil encounter and pass exhaustive fixed-allocation QA.
- [ ] Cold-boot `out/hodram_intro_english_probe_v1.nds` from New Game as Hodram;
  verify portraits, nameplates, `FI`/`FA`, wrapping, the initial objective, and normal
  progression through SC1 blocks 42-44.
- [x] Replace Lil's legacy SC2 block-27 scene with a complete 49-record,
  source-first natural-English editorial manuscript.
- [x] Complete a source-first 72-record natural-English manuscript for Lil SC2
  block 66, covering the Kamil/Antony Kuhn reunion and family-history sequence.
- [ ] Map Lil SC2 block-66 states `01/02/09/0E/14`, determine whether leading
  `28` is literal dialogue punctuation or presentation state, and measure the
  cross-route `FI` expansion before building any of its records.
- [x] Complete a source-first 35-record natural-English manuscript for Lil SC2
  block 146 without reusing the legacy batch's manual layout or guessed controls.
- [x] Replace all 156 records misidentified by the legacy Hodram route batch with
  source-locked natural-English editorial drafts across blocks 27, 66, and 146.
- [ ] Map Lil block-146 bare Kamil records, unexplained `97` lead, `FE` narration
  lead, and `FI` expansion before moving any block-146 draft into a playable batch.

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
  - [x] Phase 3: add a verified fixed-size encoder for `MESFILE`, `HELP`, and `SC0`–`SC3`.
  - [ ] Cold-boot and screenshot-test the registered `natural-dialogue-probe` profile.
    - [ ] Test Raphael block-44 records 91 through 179 for portraits, names, wrapping, and prose.
    - [ ] Test lowercase `g`, `j`, `p`, `q`, and `y` in dialogue and at least one menu.
  - [ ] Cold-boot `out/raphael_full_natural_v2_skipfix_candidate.nds` without a save state.
    - [ ] Confirm New Game reaches Choose Captain and Raphael starts normally.
    - [ ] Recheck Prince Henry, Surprised, Not yet, the complete Janus line, and the
      later tutorial scenes for blank skipped rows.
    - [ ] Continue through the tutorial choice and sample later mapped scenes in
      blocks 45-48 and 137-141 for portraits, names, wrapping, and progression.
  - [ ] Phase 4: map ILNK interior entry points and enable relocation only for proven blocks.
    - [x] Add a read-only block-layout inventory and fail-closed relocation planner.
    - [ ] Decode every interior VM continuation/event reference in Raphael block 44.
    - [x] Build and cold-boot a source-locked five-record relocation experiment.
    - [x] Revoke that experiment after it rendered one box and skipped directly to town.
    - [x] Compare failed and working VM traces and identify the 16-bit record-parity rule.
    - [ ] Cold-boot the parity-preserving five-record probe and continue beyond the scene.
    - [ ] Cold-boot the hybrid full-route candidate; confirm B44 R0034 and the later
      `Julio`, `We're`, and `Let's` continuation initials render correctly.
    - [ ] Keep route-wide expansion disabled until that probe passes and the invariant is
      confirmed on later control-flow shapes.
    - [x] Materialize and offline-audit a source-locked, parity-preserving 108-record
      natural-English expansion through the Lisbon tutorial handoff.
    - [x] Revoke `out/raphael_intro_lisbon_natural_relocation_candidate.nds`: expanded
      choice slots corrupted option two and displaced the guided tutorial entry.
    - [x] Cold-boot and accept the corrected Lisbon candidate; preserve the fixed
      tutorial-choice offsets, centered `Ask him.` / `Prepare alone.` options, and
      repaired shared crew-join message in the canonical baseline.
    - [ ] Phase 5: investigate a shared runtime Latin-renderer hook after the offline tooling is stable.
      - [x] Reject bare `0A` after cold-boot proof that it exposes the following glyph.
      - [ ] Find and cold-boot-test either a zero-width guard or an isolated progressive
        renderer hook before removing the safe `0A 20` protection.
  - [x] Phase 6: add source-locked adapters for ARM9 menus, compact HUD fields,
    packed tables, and PXL graphics.
- [x] Map and translate the packed sound selector: 38 BGM titles and all 57
  fixed-slot or standalone SFX titles.
- [x] Cold-boot the integrated Extras/Options/Sound candidate, scroll through all BGM and SFX
  entries, and confirm selection, playback, volume, and Back still work.
- [x] Rebase the coordinated Sound Setup packed-title and interior-pointer batches onto
  the accepted Raphael baseline after collecting screenshots of the remaining faults.
- [x] Keep the `sound-setup` profile experimental until those bugs are fixed and the
  user explicitly approves a complete cold-boot test.
- [ ] Route the BGM selector through the normal narrow-Latin renderer so compact
  full-width labels can eventually be replaced by complete track names.
- [ ] Replace the Options Reports/Sailing Help full-width diagnostic text with release-quality
  narrow English after its renderer adapter is implemented.

## Release discipline

- [x] Add a machine-readable accepted/experimental layer registry and mandatory build
  continuity protocol for all future models.
- [ ] Continue building every playable candidate directly from `out/raphael_natural_v2_accepted_base.nds`
  with mandatory accepted layers and a named feature profile where available.
- [ ] Require a source-locked manifest, regression verification, and cold-boot emulator test
  before promoting any candidate.
- [x] Translate and structurally guard all 21 mapped shared Trader tutorial records,
  including eight records with fixed interior entry points.
- [x] Replace the market-report fee bubble's unsafe stored newline while preserving
  both runtime `%s` substitutions.
- [x] Add 19 source-reviewed tavern and sailor-recruitment tutorial messages and
  complete editorial drafts for the six remaining concatenated records while
  quarantining them until their interior entry
  offsets are independently proven.
- [x] Complete Hodram's first Stockholm building pass: translate all mapped tavern,
  dock, and market tutorial records in SC1 blocks 134-136; repair the packed tavern
  price, hostess, rumor, and introduction entry points; and add Gerhard's omitted
  `Ardelknatts` surname slot.
- [ ] Cold-boot `out/hodram_stockholm_tavern_complete_candidate_v1.nds` from New
  Game as Hodram. Revisit the first Stockholm tavern, dock, and market; exercise
  both short tutorial choices; buy drinks, recruit sailors, and speak to Francisca;
  then confirm every portrait, nameplate, menu, wrap, and return-to-town transition.
- [ ] Cold-boot `out/raphael_tutorial_trader_complete_candidate.nds`, complete the
  guided Lisbon trading lesson, and test the Trader greeting, confirmations,
  investment prompts, market report, and return to town before promotion.
- [x] Build and independently baseline-verify
  `out/hodram_trading_complete_candidate_v1.nds` with the packed trader/tavern
  repairs, fixed-width commodity termination, mapped Lubeck labels, compact
  trading buttons, and readable town-info graphics.
- [ ] Cold-boot `out/hodram_trading_complete_candidate_v1.nds` from a full
  emulator restart and test: Stockholm trader Buy/Sell/Invest/Market Info;
  Lubeck city and market panels; Forces/Map; five-coin and Francisca tavern
  paths; Argot's rumor; and every return-to-town transition.
- [x] Map the remaining compact Japanese cargo/category captions to the shared
  marker atlas and standalone PXL strips, then translate them with source-locked
  rectangles rather than guessed ARM9 or ILNK offsets.
- [x] Audit all 810 mapped ARM9 interface/table slots and confirm that the
  `interface-polish-v1` candidate has no Japanese slots or uncovered
  high-confidence ARM9 scan hits.
- [x] Translate the 18 remaining shared marker-atlas captions plus the standalone
  Confirm, Distributed Goods, Spoils, and Temporary Storage graphics.
- [x] Reject the archival `/GRP/CMMNIMG.DK4` block-5 hypothesis after a V2
  cold-boot failure, map the six live town Common-menu sprites in
  `/GRP/DSOBJ.DK4`, and synchronize their exact 4-bpp tiles without changing
  padding rows or unrelated data.
- [x] Complete the safe COMMON gameplay campaign through block 40: replace the
  legacy filler in blocks 15-19, translate every independently addressable
  QA-clean record in blocks 20-40, and classify every remaining packed,
  identifier, macro-ambiguous, renderer-constrained, or padding-only record.
- [x] Build and independently baseline-verify
  `out/common_gameplay_natural_v2_candidate.nds`; run exhaustive dialogue QA on
  every included batch and pass the full 242-test regression suite.
- [x] Promote `out/common_gameplay_natural_v2_candidate.nds` to the canonical
  accepted baseline with a verified rollback copy and baked-layer metadata.
- [ ] Post-promotion, cold-boot `out/raphael_natural_v2_accepted_base.nds` and
  exercise naval battles, exploration, diplomacy, investment advice, treasure
  clues, taverns, Stockholm/Lubeck trading, and all menu transitions.
- [ ] Post-promotion, cold-boot `out/raphael_natural_v2_accepted_base.nds` from a full emulator
  restart. Check the title/common radial menu; Buy/Sell/Invest and cargo panels;
  confirm/storage/spoils strips; town, fleet, force, and Golden Route screens;
  world-map city/faction labels; and entry/exit transitions. Also verify that
  name entry still switches to the Latin keyboard through `英`.
- [x] Map and translate the complete Extras menu: both root choices, all four
  Online feature categories, explanatory/tie-in pages, live captions, the
  Online banner, and the thirteen baked text cards.
- [x] Cold-boot `out/extras_options_sound_common_v6_candidate.nds`; traverse every Extras and
  Online branch and verify wrapping, page order, Next/Back behavior, banner
  quality, all thirteen English text cards, the full Options label/prompts, and
  Sound Setup before promotion. Enter a city, press X, and verify every Common
  radial-menu caption and destination. Open Info and Functions and verify all
  child choices; open Deck and Assign Sailors and check the translated help,
  unclipped heading, and seven native-font plaques. Under Functions, test new
  save, overwrite, load, and empty slots; under Options, verify `Reports` and
  `Sail Help`; open Items with no inventory and verify `You have no items.`
  appears without a stray glyph.
# Dialogue presentation follow-up

- Keep protected `0A 20` breaks in playable story builds. The bare-`0A` probe failed in
  the live progressive renderer. Research a zero-width guard or an isolated runtime
  hook in a disposable probe; never weaken release encoding to test it.
- [x] Reject `out/dialogue_zero_indent_speaker_guard_probe.nds`: `0A 05` retained the
  same one-cell continuation indent in all three cold-boot screenshots.
- [x] Reject `out/dialogue_ascii_single_byte_renderer_probe.nds`: the live test still
  consumed the first post-LF glyph (`Ah.n` / `ow`, `B` / `ehold`) and retained the
  indent. The patched `0x0207CFD0` path is not the active progressive-story renderer.
- [ ] Identify the active progressive-story newline call site using an emulator runtime
  breakpoint/trace against SC0 block 44. Do not produce another bare-`0A` candidate from
  static ARM9 inference alone. Once the live call site is proved, patch only a disposable
  three-record probe and retain `0A 20` in every playable build until it passes.
- [x] Prove that `0x02172300` and `0x021723FC` through `0x02172463` are live
  structured data, not code caves; retire both builders that write there.
- [x] Locate a helper site with static and runtime ownership proof, or design a
  cave-free relocation, before another `0x020D550C` guard-skip probe.
- [x] Implement a cave-free, source-locked inline LF block rewrite with semantic,
  branch-target, mapping, and exact-diff tests.
- [x] Cold-load and reject `out/dialogue_guard_skip_inline_probe.nds`: stored
  breaks moved the first continuation glyph onto the preceding line, while an
  unrelated automatic wrap remained correctly flush left.
- [ ] Preserve `LF+SPACE` consumption and test cave-free cursor compensation or
  glyph-placement adjustment instead of skipping the guard byte.
- [x] Trace four protected breaks and prove the guard advances the cursor from
  `0` to exactly `6` before the first real continuation glyph.
- [x] Cold-load `out/dialogue_guard_cursor_inline_probe.nds`, confirm Choose
  Captain, and inspect the three stored-break fixtures plus one automatic wrap.
- [x] Reject the zero-cursor candidate after uppercase `J` disappeared at the
  left clip boundary while the remaining `anus` rendered normally.
- [x] Test the one-pixel-inset cursor candidate against `Janus` and the three
  previously repaired stored breaks.
- [x] Reject the one-pixel candidate because uppercase `J` remained missing.
- [ ] Trace the single-byte draw callback for guard space, `J`, and `a` before
  attempting another renderer patch or a reviewed wording workaround.
  - [x] Prove that the one-pixel probe submits `J` (`0x4A`) at cursor `1` and
    `a` at cursor `7`; source consumption is not dropping the letter.
  - [ ] Capture the virtual `r3` callback target and disassemble its left-edge
    clipping logic before another ROM experiment.
    - [x] Identify callback `0x020D4DA8` and confirm the embedded uppercase `J`
      bitmap is valid.
    - [x] Reject static inner target `0x020D4FC8`: the live object did not enter
      that same-method vtable candidate.
    - [ ] Read the live object's `[vtable+0x20]` target at ASCII pair dispatch
      `0x020D4FA4`, then capture the `Ja` rectangle and raster path.
      - [x] Confirm live vtable `0x021603E4` and target `0x020D4FC8`.
      - [x] Capture `[space, J]` at `(x=0, y=12)` and prove that compensated
        `a` overwrites the second-cell `J`.
      - [x] Cold-load `out/dialogue_guard_pair_phase_probe.nds`; verify New Game,
        the three original wrap fixtures, and the repaired `Janus` line.
        - User confirmed the probe worked and the complete `Janus` rendered.
      - [ ] Generalize pair-phase-safe protected breaks in the formatter and
        integrate the accepted behavior through the release-stack workflow.
- Trace the dialogue baseline/clip rectangle responsible for clipped lowercase
  descenders. The rejected glyph-upshift experiment did not solve it.
- Keep all new prose under `natural-dialogue-v2`; translate from clean Japanese with
  per-record source, context, localization, naturalness, and formatting review gates.
- Run `scripts/audit_dialogue_batch.py` and resolve or explicitly waive every warning
  before any delegated dialogue batch may enter an experimental release profile.
