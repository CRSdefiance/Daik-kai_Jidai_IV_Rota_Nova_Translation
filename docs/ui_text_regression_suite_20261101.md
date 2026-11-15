UI text regression suite — 2026-11-01

The focused suite passed on the repaired integrated candidate. No additional
rendering or navigation defect was found in the tested cases. No ROM was built,
edited or promoted during this work. Hardware acceptance remains pending.

Candidate: `out/all_routes_combined_lisbon_guild_fixed_20261101.nds`

SHA-256: `7470d392590fed3ee70d7301f42d9acdbf500e771e2191c522cec575f3c1cd94`

Its existing manifest, patch, complete V8865 content and experimental status are
unchanged. The [original repair report](lisbon_guild_hover_fix_20261101.md) records
the build provenance. This work adds test drivers, explicit expectations, replay
schedules and evidence. It does not certify every sign, custom name or game screen.

The machine-readable result is
`../tmp/ui_text_regression_20261101/suite_result.json`. Complete live evidence is
`../tmp/ui_text_regression_20261101/final_review/proof.json`; native evidence is
`../tmp/ui_text_regression_20261101/native/summary.json`.

Automated native coverage:

| Group | Passing coverage |
|---|---|
| Existing right-edge regression | 1,728 glyph cases in both pixel formats; exact original Guild header corruption detected on the unfixed reference |
| Expanded glyph/string boundaries | 3,622 cases: all 95 printable ASCII characters, supported pitches, small/zero heights, right/bottom edges, odd/even strings, exact fit/overflow and pixels stored before their header |
| Existing vertical bounds | 128 cases, including descenders and tight surfaces |
| All town labels | All 12 building types in both original layouts: 24 cases |
| Reused town label owner | 20 cycles per layout, six selections per cycle: 240 calls without restoring the owner's RAM between calls |
| Square shops | 18 complete captions and helper storage |
| Native footer | Five descriptor/stress sources; complete pixels, single cached allocation, constructor and original transfer dimensions |

The first three rows total **5,478 boundary cases**. They compare independent
expected pixels, image metadata, surrounding guards and saved-register/stack
contracts. The town tests additionally require complete visible letter cells;
clipping a legitimate word is not accepted as success. The unfixed reference must
still corrupt Guild/Ruins in both native layouts, so a test that silently stops
exercising the original bug fails.

These are isolated native CPU contracts. Supplying the other four facility IDs to
initialized Lisbon UI does not establish natural visits to those facilities.
Negative coordinates or unsupported bitmap formats are outside this suite.

Seven completed DeSmuME replays use the exact candidate bytes:

| Replay | Frames | Scope and provenance |
|---|---:|---|
| `startup` | 7,001 | Fresh New Game, captain selection, biography, confirmation and opening |
| `sailing` | 32,800 | Fresh New Game and established ordinary sailing inputs |
| `town_refit` | 17,401 | Existing Copenhagen/refit donor copied into isolated saves; inherited progression is not reverified |
| `menu_cycle_v2` | 30,800 | Lisbon radial menu, crew modes/confirmation, two item names, ship information, Save, trading, Reports and Sailing Help |
| `reload_cycles` | 11,000 | Cold boot from the save actually written through the preceding Save menu; Guild, Market, crew and inventory rehearsal |
| `repeat20` | 136,400 | Twenty complete Guild → Market → crew → inventory → town cycles using ordinary controller events |
| `results_v2` | 28,400 | Existing five-ship donor; battle, victory text, rewards, cargo tooltips/headings and confirmation warnings |

Total: **263,802 frames**, **171 complete live glyph masks**, **five exact-region
comparisons**, and a blank-band check below confirmation text. The biography's
three Y coordinates and 12-pixel spacing are explicitly checked. The repeated
cycle contributes 100 scheduled masks; each cycle must reach five distinct
expected display states. Completing frames or producing video callbacks alone is
not considered navigation success.

Trading preview changes Income from zero to four digits. Cancel/reopen must
restore the entire checked Net panel exactly, including its zero values. Crew
mode changes exercise short/long numeric displays and return to the original
stats. Cold-loaded item title/description and ship/crew regions must equal their
pre-save counterparts. The exact live quantity examples 9→10 and 99→100 were not
separately exercised; numeric width changes and the common drawing boundaries
were tested instead. No committed purchase is needed for the preview/reset check.

The results replay explicitly reuses two approach-coordinate fixtures, each
owning eight bytes. They do not set health, inventory, rewards or an outcome.
Original simulation reaches the result screens. The current collision routine,
whole decoder overlay and world-map asset are checked against clean source before
requalifying the existing fixture. This run does not prove earned travel or the
donor's earlier progression. Other completed replays enable no new gameplay
fixtures. None loads a savestate. Every source battery remains unchanged.

Every completed replay verifies the final clipping instructions and all 4,088
immutable bytes of the 4,096-byte helper section. Only two declared four-byte heap
cache slots may change. Both pointers must remain within owned RAM extents; an
initialized Market cache must have its original 184×36, 4-bit header, pixel offset
and palette. Unexpected neighboring writes remain failures.

The focused pytest run passed **63 tests**, including 15 tests that challenge the
cache guard with changed instructions, neighboring writes, malformed headers and
out-of-range allocations. The remaining tests cover the existing integrated
release, translation integrity, ASCII guard and dialogue pair-phase contracts.
All four new Python drivers compile successfully.

Initial failing expectations are preserved:

- Older V654 result wording/timing and an `Undo` expectation did not describe the
  current replay. Directly reviewed captures establish the current full sentences,
  reward timing and `Unload` caption. Active result expectations are v2.
- `Route Map` and `Crew Setup` match the original font at five-pixel advance;
  the revised font is the wrong oracle for those exact masks. They now have an
  explicit original-font expectation; other masks still use the candidate font.
  Font matching alone is not used to infer the resource or rendering path.
- The original helper check allowed only the footer cache word. Entering Market
  initializes the already-declared second cache at `0x01FFC680`. Its native
  allocation and header were traced to
  `scripts/prepare_commodity_private_market_v353.py` and validated in actual RAM.
  No arbitrary changed region was exempted.
- Ship-list/Lookout bounds and the Save menu's foreground color were qualified
  from their current captures. The earlier failed proofs/logs remain separate.

Representative startup, refit, sailing, menu, save, trading, result, and first/last
repeat-cycle screenshots were directly viewed. The full 100 repeat masks are
automated pixel evidence; they are not 100 separate manual visual reviews.

Reusable drivers and active fixtures:

- `scripts/verify_ui_text_regression.py`: native tests from the supplied ROM;
  rejects an ARM9 that differs from the qualified repaired runtime instead of
  silently substituting a historical compiled target.
- `scripts/run_ui_text_smoke.py`: fresh isolated cold boots, scheduled or
  interactive ordinary inputs, recorded ROM/input/save identities, declared
  results-only fixtures and source-battery checks.
- `scripts/create_ui_text_cycle_schedule.py`: verifies the completed rehearsal's
  landmark pixels and generates the twenty-cycle input schedule.
- `scripts/review_ui_text_smoke.py`: verifies capture identities, complete masks,
  placements, blank bands, region comparisons and runtime storage.
- `tests/fixtures/ui_text_smoke_checks_v1.json`,
  `ui_text_results_checks_v2.json`, `ui_text_menu_checks_v2.json`: active fixed
  expectations. Earlier v1 menu/result files are diagnostic history.
- `tests/fixtures/ui_text_menu_inputs_v1.json` and
  `ui_text_reload_inputs_v1.json`: completed ordinary-input schedules, allowing
  the exploratory menu/cold-load paths to be replayed without manual navigation.
- `../tmp/ui_text_regression_20261101/suite_checks.json`: the combined 171-mask
  plan, including generated repeat-cycle checks and vertical/blank-band checks.

Run from the repository root with the configured Python dependencies. Always use
a new output folder; the drivers reject existing evidence folders. For example:

```text
python scripts/verify_ui_text_regression.py --rom out/all_routes_combined_lisbon_guild_fixed_20261101.nds --expect-sha256 7470d392590fed3ee70d7301f42d9acdbf500e771e2191c522cec575f3c1cd94 --out ../tmp/ui_text_recheck/native

python scripts/run_ui_text_smoke.py --rom out/all_routes_combined_lisbon_guild_fixed_20261101.nds --expect-sha256 7470d392590fed3ee70d7301f42d9acdbf500e771e2191c522cec575f3c1cd94 --flow sailing --out ../tmp/ui_text_recheck/sailing

python scripts/review_ui_text_smoke.py --rom out/all_routes_combined_lisbon_guild_fixed_20261101.nds --expect-sha256 7470d392590fed3ee70d7301f42d9acdbf500e771e2191c522cec575f3c1cd94 --root ../tmp/ui_text_regression_20261101 --checks ../tmp/ui_text_regression_20261101/suite_checks.json --out ../tmp/ui_text_recheck/review
```

For a fresh Save/load replay, use the menu schedule with `--flow schedule`,
`--frames 30800`, the original isolated Lisbon donor and the expected capture
frames. Copy its completed save to a new snapshot, then run the reload schedule
for 11000 frames. The snapshot used here is
`../tmp/ui_text_regression_20261101/post_save_snapshot.dsv`, SHA-256
`eeba875dd69286b1610938eebffee34d9860c49526db3ebe4c6777d05771f887`.
The native fixtures and recorded input assets must be retained. A different
runtime or changed fixture requires explicit requalification, not bypassing a
failed identity check.

Short 3DS acceptance checklist, using the repaired ROM and a spare save slot:

1. Cold boot the Lisbon save. Hover Guild, move away, enter and return.
2. Open the radial menu, Crew Setup and Items. Change selections and return;
   check long item names and complete button letters.
3. Open refit and, when available, sailing. Check `Finish`, `Undo`, `Edit`,
   `Rotate`, `Inspect` and `Sails`, including the bottom of the `p`.
4. Preview a trade, cancel and reopen. Check that totals and labels reset cleanly.
5. Save to the spare slot, close the game, cold boot and Continue. Check names,
   crew/ship fields and ordinary navigation again.

Remaining limits: no physical 3DS verification, full playthrough, exhaustive
custom-name/widget matrix, all rare event screens, every possible numeric extreme
or certification of all decorative sign assets. This suite provides evidence for
the shared drawing boundaries and representative UI behavior, not a numerical
probability that the whole game is defect-free.

Retention preview `work/rom_retention/20261101T1638187281331Z.json` again proposes
210 deletions. It was not applied: the previously documented unresolved active
dependency audit still holds. No ROM was created or deleted by this test work.
