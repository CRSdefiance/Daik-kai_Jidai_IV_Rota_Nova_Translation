# Project to-do list

## High priority

- [ ] Cold-boot `out/shipyard_complete_v1_candidate.nds` and exercise Repair,
  Remodel, every equipment-room tile, Y Reset/Yes/No, Back/Yes/No, Rename, ship
  swapping with empty slots, and ship purchasing. Confirm both Repair responses
  retain their first letters; packed helper/discount/rename messages select the
  correct English entry; all descriptions wrap cleanly; empty slots read `Ship 2`
  through `Ship 5`; and Saker, Culverin, Pedrero, Cannon, Heavy Cannon, and
  Carronade remain separated from their runtime gun counts.

- [x] Cold-boot `out/ships_submenu_v1_candidate.nds`; confirm the native labels,
  English `Cpt.`, `Culverin 24` spacing, values, and navigation, while rejecting
  the remaining beige fields behind the cargo and cannon sprites.
- [ ] Cold-boot `out/ships_submenu_v2_candidate.nds` and inspect Common > Info >
  Ships with cargo and a Culverin. Confirm `Cargo` clearly owns the two native
  item thumbnails, `Fore/Aft` and `Square` are readable, the cannon thumbnail
  precedes `Culverin 24`, all values remain aligned, and Back works.
- [ ] Cold-boot `out/ships_route_forces_v1_candidate.nds` from a full emulator
  restart. On the route map, inspect Hamburg, Amsterdam, Hangzhou, Quanzhou,
  Nagasaki, and Tsukushi plus cities in several regions; confirm all names are
  English and each coordinate pair occupies a clean second line. Open Forces
  and confirm the source-textured native-font plaques, English leader/region and
  unknown-force text, English Hayreddin/Silveira/Uddin/Centurione groups, and
  complete Area/Map/Back buttons. Open World Map and switch between Area and
  Fleet/Town; confirm its title, instructions, and Switch/Area/Back/Done buttons
  remain fully English. Repeat the Ships V2 checks before promotion.
- [ ] Cold-boot `out/opening_movie_v1_candidate.nds` from a full emulator restart.
  Let the complete opening movie run: verify both cyan title prompts, the newly
  translated Clau subtitle, and the opaque black outline on all five English movie
  cards over light and dark frames. Start each captain once and confirm the animated
  English name captions and transitions are unchanged. Repeat the Ships, route-map,
  Forces, and World Map checks inherited from the combined candidate.

- [x] Correct route ownership: SC1 is Hodram's playable route; SC2 is Lil's. Revoke
  the inaccessible wrong-route SC2 control probe and retain its ROM only as evidence.
- [x] Translate 67 records from Hodram's actual SC1 opening through the first
  Lil/Kamil encounter and pass exhaustive fixed-allocation QA.
- [ ] Cold-boot `out/hodram_intro_english_probe_v1.nds` from New Game as Hodram;
  verify portraits, nameplates, `FI`/`FA`, wrapping, the initial objective, and normal
  progression through SC1 blocks 42-44.
- [x] Replace Lil's legacy SC2 block-27 scene with a complete 49-record,
  source-first natural-English editorial manuscript.
- [x] Translate all 35 dialogue and system records in Lil SC2 block 23, covering
  Kamil's Deck-post tutorial immediately after the opening voyage.
- [x] Build a one-record, fixed-allocation probe for Lil's first visible Amsterdam
  line (`SC2 B22 R0019`) without enabling the revoked full-opening batch.
- [ ] Cold-boot `out/lil_b22_first_screen_probe_v1.nds` from New Game as Lil and
  verify her portrait/nameplate, the first English glyph, all three lines, and the
  transition to Kamil's following Japanese line.
- [x] Encode all 49 source-reviewed lines in Lil's Amsterdam opening as a new
  fixed-allocation B22 intro candidate, preserving the four speaker selectors and
  route-name macro without reusing the revoked legacy batch.
- [ ] Cold-boot `out/lil_b22_intro_natural_v2_candidate.nds` through the complete
  Amsterdam departure and verify every portrait, nameplate, page break, scene
  transition, and the handoff into the Deck-post tutorial.
- [x] Statically map SC2 block-23 selectors `02/09/14/FE`, identify records 18
  and 20 as bare choice labels, correlate the surrounding choice grammar, and
  resolve Lil-route `FI/FA/FO` defaults.
- [ ] Cold-boot the seven-record `lil-b23-control-probe` and verify portraits,
  nameplates, both choice positions and branches, `FI` expansion, system-panel
  rendering, and return to normal tutorial flow before making B23 playable.
- [x] Complete a source-first 72-record natural-English manuscript for Lil SC2
  block 66, covering the Kamil/Antony Kuhn reunion and family-history sequence.
- [ ] Map Lil SC2 block-66 states `01/02/09/0E/14`, determine whether leading
  `28` is literal dialogue punctuation or presentation state, and measure the
  cross-route `FI` expansion before building any of its records.
- [x] Complete a source-first 35-record natural-English manuscript for Lil SC2
  block 146 without reusing the legacy batch's manual layout or guessed controls.
- [x] Replace all 156 records misidentified by the legacy Hodram route batch with
  source-locked natural-English editorial drafts across blocks 27, 66, and 146.
- [x] Map Lil block-146 Kamil `09` records, `97` sailor lead, `FE` narration
  lead, and both `FI` macros; encode all 35 records with exact control checks.

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

## Lil route continuation

- [x] Source-review and encode all 36 SC2 B105 Sphinx-riddle records with natural
  American English, preserving the `CF` party state and the first English glyph
  of each choice label.
- [x] Build `lil-deep-route-v26` from the accepted integrated base; audit all 36
  records, review their previews, verify their exact candidate bytes, and pass the
  baseline invariant check.
- [x] Source-review and encode the complete 45-record B106 cult confrontation
  and 10-record B108 hidden-believer lamp scene; verify `89` text starts and
  preserve the `A0`, `B1`, and `B2` presentation states.
- [x] Build and verify the experimental `lil-deep-route-v27` candidate; inspect
  its 55 exact new SC2 records and confirm the accepted-base invariant.
- [x] Translate all 16 spoken records in SC2 B107 and leave its four-byte
  opening fragment unchanged as an explicit control-map exclusion.
- [x] Verify V28's 16 exact dialogue records and the unchanged fragment in the
  integrated candidate; pass the baseline and manifest checks.
- [x] Source-review all 73 B109-B110 Colosseum riddle and urn-puzzle dialogue
  records; preserve the party and voice states, both `FI` name macros, and the
  first visible character of every ordinary-text choice and companion variant.
- [x] Build the experimental V29 candidate; visually review every new preview,
  pass the 73-record audit and 14 Lil tests, verify exact ROM bytes and the
  accepted-base invariant, and leave B109 R0281 byte-identical.
- [x] Source-review and encode all 33 spoken B111 gold-temple monk records with
  the scene-scoped `89` state and Kamil's `FI` macro; leave the two punctuation
  records unchanged as explicit exclusions.
- [x] Build and verify the experimental V30 candidate; review all B111 previews,
  pass 16 targeted Lil tests and Ruff, verify 33 exact new records and the 73
  V29 records, and pass the accepted-base invariant.
- [x] Translate all 30 spoken B112 rescue records, preserve the child,
  grandfather, lookout, and rescuer states, and verify the first English glyph
  in every ordinary-text companion variant.
- [x] Build and verify experimental V31; review all previews, pass 18 Lil tests,
  exact-record and manifest checks, and the accepted-base invariant. Leave
  B112 R0010 unchanged pending scene-control mapping.
- [x] Translate the six B113 jade-discovery and thirteen B114 cacao-follow-up
  dialogue records, preserve the townsman's `68` state, and keep both B113
  non-prose fragments unchanged as explicit exclusions.
- [x] Build and verify experimental V32; review all previews, pass 20 targeted
  Lil tests and Ruff, verify all 19 new and 30 V31 exact records, and pass the
  accepted-base invariant and manifest checks.
- [x] Translate all 37 B115 tablet and shared Maria recruitment records; preserve
  speaker states, the faction macro, and the opening `B` after source LF staging.
- [x] Build and verify experimental V33; review all 37 previews, pass 22 targeted
  Lil tests and Ruff, verify 37 V33 and 19 V32 exact records plus unchanged
  exclusions, and pass the accepted-base invariant and all 13 manifest checks.
- [x] Translate 30 B116-B118 India-tip, figurehead, and tribal knife-reward
  records. Preserve C6/D1/DC/B3 states and both non-prose staging fragments.
- [x] Build and verify experimental V34; review every preview, pass 24 targeted
  Lil tests and Ruff, check 30 V34 and 37 V33 exact records and both exclusions,
  and pass the baseline invariant and all 13 manifest checks.
- [x] Complete B120 with 28 new natural-English sailing-tutorial records,
  retaining both FI macros and the inherited V21 refusal.
- [x] Build and verify experimental V35; review all previews, pass 26 targeted
  Lil tests and Ruff, verify all 29 cumulative B120 records, preserve 30 V34
  records and its exclusions, and pass all manifest and baseline checks.
- [x] Complete all 109 B121 ambush, rescue, Kamil reconciliation and farewell
  records with natural English, preserved presentation states and ten FI macros.
- [x] Build and verify experimental V36; review all previews, pass 28 targeted
  tests and Ruff, verify all new records and inherited B120 records, and pass
  all 13 manifest checks and the baseline invariant.
- [x] Finish the current B122 Clifford farewell scene (30 records), preserve
  three FI macros and 02/09/97/FE presentation states, and review all previews.
- [x] Pause Lil at the user's request and compile the four-route cumulative
  candidate with Raphael V93, Hodram V32, Maria V111 and Lil V37.
- [x] Resume at the user's request and translate all 22 B123–B124 Christina
  invitation and Julian tavern-advice records into natural American English.
- [x] Review every B123–B124 preview and build the four-route V4 candidate;
  pass 35 targeted tests, Ruff, all 13 manifest checks, the baseline invariant,
  and exact saved-record verification for all four routes.
- [x] Complete all 44 B125 moral-doubt, two-choice, Guiding Staff and spirit
  reward records; audit every preview and preserve FI and choice starts.
- [x] Complete all 15 B126 Bruges trading-tutorial records with accurate
  cargo-hold and market-share instructions and both response branches.
- [x] Build and verify the four-route V6 candidate; pass 39 targeted tests,
  Ruff, all 13 manifest checks, baseline invariant and exact saved-record
  verification across Raphael, Hodram, Lil and Maria.
- [x] Source-review all 145 B127–B132 Lil dialogue records: Fernando's
  card game, Martin Speyer and both responses, market-share mechanics,
  Amsterdam polder, Clifford's map key and southern trade warning.
- [x] Review every new exact-font preview and build combined V10; pass 41
  targeted tests, Ruff, all 13 build checks, hashes, baseline invariant,
  and exact saved-record verification. Preserve B131 R0080 unchanged.
- [x] Source-review, audit, preview and build B133–B136, including both B133
  and B134 choice paths, the Espinosa scene, and the Africa tablet map;
  preserve B136 R0020 unchanged as an opaque event payload.
- [x] Source-review, audit, preview and build all 47 B137 Nagalpur tavern
  records, retaining FI macros, the fivefold-wage challenge and Lil's reply.
- [x] Source-review, audit, preview and build all 55 B138–B139 dialogue
  records, including both treasure-map price branches, the leaf handoff,
  and the platter map reveal; preserve opaque B139 R0035 unchanged.
- [x] Source-review, audit, preview and build all 101 B140–B145 text records:
  Lil's polder pledge and funding branches, shipyard armor research and
  completion, and the Mediterranean Proof map reveal; preserve the opaque
  B145 R0021 event payload unchanged.
- [x] Source-review, audit, preview and build all 35 B146 Kamil/Hodram
  dialogue and narration records, preserving the two `FI` macros.
- [x] Source-review, audit, preview, and build all 68 B147 text records for
  Maria's identity reveal and warning about Kuhn; preserve the opaque R0129
  event payload unchanged and verify first glyphs in individual previews.
- [x] Source-review, audit, preview, and build all 45 B148-B149 dialogue
  records: Kamil's identity clue and both Tang Bamboo Craft puzzle branches.
- [x] Source-review, audit, preview, and build all 22 B150 Clifford alliance
  dialogue records, retaining the `FO` faction macro.
- [x] Source-review, audit, preview, and build all 55 B151 Maldonado tavern
  dialogue records, including alternate monologues and crew branches.
- [x] Source-review, audit, preview, and build all 15 B152-B153 coin-map
  dialogue records; preserve the opaque B153 R0024 event unchanged.
- [x] Source-review, audit, preview, and build all 40 B154 Al recruitment
  dialogue records; preserve the opaque R0003 scene event unchanged.
- [x] Source-review, audit, preview, and build all 48 B155 Angelo recruitment
  and African trade records; preserve the opaque R0059 scene event unchanged.
- [x] Source-review, audit, preview, and build all 69 B156 Ian Dukov tavern,
  ambush, rescue, and recruitment records.
- [x] Source-review, audit, preview, and build all 70 B157 Carlo Sinato
  market, family loss, and recruitment records.
- [x] Source-review, audit, preview, and build all 19 B158 Christina tavern
  dance records, including audience cheers and applause.
- [x] Source-review, audit, preview, and build all 41 B159 Samwell market,
  cooking-trial, and recruitment records; preserve the opaque R0045 event.
- [x] Source-review, audit, preview, and build all 23 B160-B162 stolen-ship
  discovery and dockworker-update records; preserve the FI macro and all
  speaker presentation leads.
- [x] Source-review, audit, preview, and build all 43 B163 ship-return and
  Jam Jack Ludwyan recruitment records; preserve opaque R0034 unchanged.
- [x] Source-review, audit, preview, and build all 52 B168 Mikhail
  recruitment and item-information tutorial records; preserve FI, FA, and
  FO name macros and all nine speaker presentation leads.
- [x] Source-review, audit, preview, and build all 36 B169 Proof of
  Conqueror explanation and search-advice records; preserve five FI and
  two FO name macros.
- [x] Source-review, audit, preview, and build all 33 B170 Yifa recruitment
  records; preserve the FI and FO name macros.
- [x] Source-review, audit, preview, and build all 35 B171 Sanghyeon dream
  and Yifa training records; preserve the FI name macro and new 51 lead.
- [x] Source-review, audit, preview, and build all 27 B172 Golden Crown of
  Silla lead records; preserve all speaker presentation leads.
- [x] Source-review, audit, preview, and build all 44 B173-B174 Golden Crown
  tomb lead, crown handoff, and Julian recruitment records; preserve all
  speaker presentation leads including the Seoul tavernkeeper's `CA`.
- [x] Source-review, audit, preview, and build all 32 B175 Aziza pirate
  confrontation dialogue records; preserve the FI and FA name macros
  and exclude the opaque four-byte event payload unchanged.
- [x] Source-review, audit, preview, and build all 10 B176 Seville
  banana-boom records; preserve the AE and AF presentation states.
- [x] Source-review, audit, preview, and build all 10 B177 Genoa
  tomato-boom records; preserve the AE and AF presentation states.
- [x] Source-review, audit, preview, and build all 13 B178 Amsterdam
  wheat-boom records; preserve the new A8 neighbor presentation state.
- [x] Source-review, audit, preview, and build all eight B179 San Jorge
  wine-boom text records; preserve the drinker, barkeep, and notice leads.
- [x] Source-review, audit, preview, and build all 29 B180-B182 Lisbon
  spice, Athens ruby, and London gem rumor records.
- [x] Source-review, audit, preview, and build all 25 B183 Basra
  painting-craze records, including the short 99 interjection and FE door cue.
- [x] Source-review, audit, preview, and build all 29 B184-B186 Sofala
  tea, Stockholm fur, and Alexandria sweets market records.
- [x] Source-review, audit, preview, and build all 16 B187 Malacca
  almond-medicine rumor records; preserve 9B, 57, and FE presentation leads.
- [x] Source-review, audit, preview, and build all 11 B188 Osaka
  giyaman-glass market records; retain 82/96 as text leads and FE as notice.
- [x] Source-review, audit, preview, and build all 17 B189 Hamburg
  ceramics collector and swindler records; preserve 93/52/68/71/FE states.
- [x] Source-review, audit, preview, and build all 17 B190 Havana
  medicine-rumor records; preserve 9F/77/FE presentation states.
- [x] Source-review, audit, preview, and build all 13 B191 Calicut
  father-son dye-market records; preserve 56/9A/FE presentation states.
- [x] Source-review, audit, preview, and build all 33 B192-B194 Istanbul
  tobacco, Seoul chili, and Hangzhou sake records; preserve the FI name macro.
- [x] Source-review, audit, preview, and build all 20 B195 Veracruz
  cheese-dish market records; preserve 77/67/5C/FE presentation states.
- [x] Source-review, audit, preview, and build all 35 B196 haggling records,
  including six Buy/Pass pairs, the FI reward, and every price branch.
- [x] Source-review, audit, preview, and build all 24 B197 celestial-maiden
  book records, including Buy it/Pass/Trust choices and the charm reward;
  preserve the one packed event payload unchanged.
- [x] Source-review, audit, preview, and build all 15 B198 namahage dream
  records, including the repeated challenge and mysterious-object discovery.
- [x] Source-review, audit, preview, and build all 31 B199 portrait and book
  text records, preserving the FI name macro and one packed event unchanged.
- [x] Source-review, audit, preview, and build all 19 B200 Carlo and
  collapsed-traveler records, including the gift and charm reward.
- [x] Source-review, audit, preview, and build all 25 B201 enchanted
  mast-rope bargaining records, both choices and the three stat notices.
- [x] Source-review, audit, preview, and build all 19 B202 Glassmaking
  Guide records, preserving the stranger, pursuer, Lil, and Charles states.
- [x] Source-review, audit, preview, and build all 21 B203 caterpillar-
  fungus and medicine-book records, both prices, and the FI charm reward.
- [x] Source-review, audit, preview, and build all 20 B204 shachihoko
  records, including the castle retainer, lord, and Jam's signed letter.
- [x] Source-review, audit, preview, and build all 17 B205 talking-parrot
  text records, preserving one packed parrot event unchanged.
- [x] Source-review, audit, preview, and build all 28 B206 ceramic-earrings
  text records and four bare choices; preserve one packed item event.
- [x] Source-review, audit, preview, and build all 126 B207-B214 optional
  treasure-scene text records, all letter variants and five choices.
- [x] Complete the Lil translation route: 6,539 translated records, zero remaining,
  69 preserved native controls; combined V123 ROM verified. Runtime acceptance pending.
- [x] Translate and verify B316: 94 texts, ten sheets and unified V118 saved-ROM checks.
- [x] Translate and verify B317-B319: 35 texts, four sheets and unified V119 saved-ROM checks.
- [x] Translate and verify B323: 66 texts, four packed exclusions, seven sheets and unified V120 saved-ROM checks.
- [x] Translate and verify B324: 59 texts, three packed exclusions, six sheets and unified V121 saved-ROM checks.
- [x] Translate and verify B325-B329: 54 texts, three packed exclusions, six sheets and unified V122 saved-ROM checks.
- [x] Translate and verify B330-B335: 77 texts, eight sheets; classify three B22 controls and verify unified V123.
- [x] Translate and verify all 23 B295-B298 wristband quest records, three sheets and unified V111 saved-ROM checks.
- [x] Translate and verify all 103 B299-B300 snake and bog records, 11 sheets and unified V112 saved-ROM checks; preserve packed event.
- [x] Translate and verify all 85 B301-B305 desert and spice records, nine sheets and unified V113 saved-ROM checks.
- [x] Translate and verify B306-B311: 83 text records, two packed exclusions, nine sheets and unified V114/V115 saved-ROM checks; separate real 97 from Japanese 97AC.
- [x] Translate and verify B312-B313: 84 text records, two packed exclusions, nine sheets and unified V116 saved-ROM checks.
- [x] Translate and verify B314-B315: 38 text records, two packed exclusions, four sheets and unified V117 saved-ROM checks.
- [x] Translate and verify all 98 B293-B294 fog and cliff text records, ten sheets and unified V110 saved-ROM checks; preserve two packed events.
- [x] Translate and verify all 51 B289-B292 Angkor records, six sheets and unified V109 saved-ROM checks; preserve two packed events.
- [x] Translate and verify all 82 B288 cave encounter records, nine sheets and unified V108 saved-ROM checks.
- [x] Translate and verify all 104 B283-B287 text records, 11 sheets and unified V107 saved-ROM checks; preserve packed forest event.
- [x] Translate and verify all 154 B255-B282 guild quest records, 16 preview sheets and unified V106 saved-ROM checks.
- [ ] Cold-boot the cumulative Lil candidate through the temple, both Sphinx
  riddles and answer branches, the cult confrontation, temple star clue,
  hidden-believer lamp scene, Colosseum bean riddle (all three answers), and urn
  choices, the gold-temple monk exchange, sandbar rescue, jade discovery, and
  cacao follow-up with gate unlock, tablet scene, and Maria's raider recruitment;
  the India building tip, figurehead discovery, tribal knife reward, and first
  sailing tutorial through all answers and arrival in Bruges; both ambush choices
  and rescue branches, Kamil's return and the Proof-map key farewell;
  Clifford's burning ship, farewell and letter reward;
  Christina's grandfather/London invitation and Julian's tavern advice;
  both Lil/Kamil moral-doubt answers, Guiding Staff clue and spirit reward,
  then both Bruges trading lessons and cargo/market-share instructions;
  check the faction expansion, portraits, choices, first
  glyphs, and transitions
  before accepting or promoting it.

- [x] Translate and verify Lil B215-B226: 155 records, 16 preview sheets, zero dialogue blockers, combined V102 saved-ROM verification.

- [x] Translate and verify Lil B227-B238: 166 records, 17 sheets, zero audit blockers, combined V103 saved-ROM verification.

- [x] Translate and verify Lil B239-B249: 135 records, 14 sheets, one unchanged packed event, combined V104 saved-ROM verification.

- [x] Translate and verify Lil B250-B254: 83 records, nine sheets, one unchanged curse control, combined V105 saved-ROM verification.
