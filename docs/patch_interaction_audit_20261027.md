# Patch interaction audit — 2026-10-27

The representative audit found **no additional confirmed ROM defect** beyond the Lisbon Square collision already repaired. No further ROM bytes were changed during this audit. The candidate remains experimental; cosmetic work and promotion remain paused. This is bounded regression evidence, with the coverage gaps below still open.

Follow-up: all ten historical test blockers are now resolved with exact original
ROM identities and unchanged assertions. The final targeted run passes86 tests
across13 files; combined audit evidence is2457 passes/seven skips across493
files. The earlier blocked checkpoint below is retained as history. See
[fixture recovery and final receipts](blocked_test_resolution_20261027.md).

## Exact target and preservation

- Candidate: `out/font_v2_square_scratch_fix_20261027_test.nds`.
- SHA-256: `89860905d61e348ae053d40836159bc86bff5d85d3206ce3a0961a6d60142077`.
- Registered profile: `font-v2-square-scratch-fix-20261027`; neighboring manifest has560 batch entries and preserves114 accepted layers.
- Release-stack SHA-256: `c54902e5c82bf84fa16830f94dc200702308faa7af09509bcb53f84c4ba2ddf4`; its bytes remain identical to the audit-start snapshot.
- Canonical baseline remains `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`. The promoted main was not changed.
- Full registered reconstruction reproduced the candidate exactly. The trace records190 ARM9 replacement stages and6933 final writer ranges. Build write provenance is distinct from runtime ownership.
- No files under `sources/` were changed. All donor saves were copied into isolated sessions; their original hashes were checked afterward. No save state was loaded.

The prior repair moves the Square painter's448-byte temporary bitmap onto its stack. It prevents Square from overwriting the font helper at`01FFC200..01FFC300`. Its18 native complete-caption cases, four fallbacks, ABI/restoration checks and earlier cold-boot Square controls remain documented in [the original diagnosis](lisbon_square_freeze_20261027.md). The earlier three one-pixel builds remain revoked. Cold-boot the repaired build; loading the frozen state restores damaged memory.

## Memory ownership and patch interactions

Five ARM9 autoload sections are disjoint, including the hardware-mirrored ITCM ranges. Native SDK arena initialization/getters and the main-pool startup copy/cache contract pass. The native main arena begins exactly after the relocated123040-byte patch pool. The staging copy lies in memory that can be reused after startup; it is not treated as permanently reserved patch storage. The overlay window is separate from the added ITCM helper block.

The audit collected282 registered configuration declarations,1631 transitive source dependencies and189 conservative ITCM reference leads. Those counts include historical producer dependencies and data aliases; they are not counts of active patches or confirmed defects. Zero-filled bytes were not accepted as proof of ownership.

At 189 same-frame memory snapshots across 26 captured attempts, the checker compared:

| Area | Bytes compared per snapshot | Result |
|---|---:|---|
| Added ITCM helper block |4096|Only two declared cache-pointer words changed.|
| Relocated patch pool |123040|Only the18 Square bitmap slots changed.|
| Changed main ARM9 bytes relative to clean Japanese |39958|Only six town-stock cache words changed.|
| Changed older ITCM bytes relative to clean Japanese |1251|No changes.|

The DTCM section is byte-identical to clean Japanese; this audit adds no DTCM patch. Main-code comparison covers changed bytes, not every original runtime global. Snapshots sample transitions rather than tracing every write between frames.

Explicit mutable allocations, with exclusive ends:

| Owner | Range | Lifetime and evidence |
|---|---|---|
| Footer image pointer |`01FFC2D8..01FFC2DC`|One lazy native1792-byte allocation; source/current helper contract.|
| Market private image pointer |`01FFC680..01FFC684`|One lazy native4096-byte allocation; current constructor allocates, initializes and stores this pointer.|
| Square caption canvases |`023991E0..0239AF20`|18 slots of416 bytes, allocated in the registered pool.|
| Town-stock row cache |`0215DC24..0215DC3C`|Five row pointers plus a count; the following self-pointer literal stays protected.|

Direct Market testing initially tripped the strict checker at`01FFC680`. Investigation proved this was the existing private-image cache, not overwritten instructions: the current allocation/store instructions match its source, the observed image has the expected184×36 header/palette, and repeated visits reuse the same pointer. The neighboring fleet-label allocation ends before this word. Both cached heap allocations stay within the native heap and do not overlap each other or the relocated pool in the observations. The checker now recognizes this precise owner; it does not exempt neighboring bytes.

Protected-address negative ownership controls pass. Current evidence contains no unexpected mutable/code overlap. This does not certify every future route state or every allocation lifetime after untested transitions.

## Actual emulator coverage

24 completed headless DeSmuME sessions advanced 408958 frames with zero callback errors: 23 representative replay/control sessions plus one encounter-readiness probe. Captures come from the actual candidate's framebuffer. All 24 representative sheets and additional identified direct screens were visually reviewed; not every captured frame was individually reviewed. Each session retains its inputs, command journal, screenshots, RAM/native exports and capture report.

| Area | Observed result and boundary |
|---|---|
| Guild |Seoul purchase/sale dialogs, changed funds and town return.|
| Inn |One/three-night stays, date/funds changes and return.|
| Palace |Contract fee/share dialogs, accepted contract and return.|
| Market |Contract refusal before signing; actual trade/confirmed cargo sale afterward, funds5299→8071; price/category pages; return.|
| Tavern/recruitment |Welcome/drink dialog, recruitment offer/answer, sailor/capacity dialog and return.|
| Square |Shop captions, portraits, trends and conversation progress; no freeze.|
| Shipyard/refit |Last-ship sale refusal, equipment grid/descriptions/choices and return to remodeling menu. Ship construction/purchase and every repair branch are not covered.|
| Port |Actual Depart/Dock/Cargo Setup menu, cargo grid/navigation, Dock/Swap Ships and town return.|
| Church |Prayer answer, peace response and repeated visit/return; prepared calendar/facility prerequisite.|
| Title/Options |Sound Setup names/controls and preview requests, Report/Sailing Help prompts, captain selection/back, Extras/About/Online pages and title return. Audible output was not assessed.|
| Help/save loading |Help pages and town return; load selection and actual transition from Syracuse to saved Stockholm. Saving/overwriting every slot is not covered.|
| Gallery/Grand Race |Multiple portraits/names and return; host waiting roster and return to title. Prepared unlocks; no wireless race.|
| Sailing/fleet menus |Sea View, ship inspection, Deck/Lookout duty selection, Fleet Info and ship-detail pages, return to sailing.|
| Naval battle/duel |Encounter/tutorial conversation, ordinary engagement, changing crew/supplies and disengagement. A separate current-ROM replay reaches duel challenge/acceptance, visible fencing combat with falling HP, enemy-flagship flight/victory speech, aftermath and Gerhard's level-up/sea return. Alternate outcomes are not exhaustive.|
| Raphael route |Ask him choice, Julio conversations and initial town tutorial handoff; not the complete tutorial/crowd event.|
| Hodram route |Opening choice, crew/Manuel conversations and Stockholm town.|
| Lil route |Amsterdam opening, Fernando/permit conversations and initial sailing handoff.|
| Maria route |Ian/Xien/Yukihisa opening conversations, Hangzhou town and Tavern; prepared system unlock.|
| Additional route event |Istanbul Angelo encounter, scripted duel conversation/illustrations, joining message and return to Port. This is not interactive duel coverage.|

The old replay names overstated some coverage: `port` and `shipyard` both reached the Yard sale refusal; `town_market_tavern` reached Maria's opening/Tavern. They were relabeled in the evidence, and the missing Market/Port visits were performed directly.

Battle and Church use explicitly bounded prerequisite fixtures in copied RAM. The battle approach owns 40 own-fleet position bytes; the Church control owns only a calendar word and facility mask. The duel/aftermath replay additionally prepares original diplomatic/attack-order prerequisites, contact position, positive health, native attributes and equipment in disposable state. Its original native consumer/bounds, actor identity, current-message/component/cache/directory, RNG and outcome exclusions remain intact. All 31 prerequisite applications end at frame 5770, before the visible duel challenge at 5782; none occur during combat or afterward. The native game produces the victory/result. These are prepared conditions, not naturally earned travel, availability, abilities or unlocks. Gallery/Race/Maria also inherit prepared battery prerequisites.

## Regression tests and unsuccessful attempts

492 test files were run in separate processes. **482 files passed**, comprising 2396 passed tests and seven skips. Ten files remain blocked, producing 12 failures and 35 setup errors; all 47 terminal exceptions are `FileNotFoundError` for unavailable historical inputs. The complete suite is therefore **not green**, and unavailable fixtures are not counted as passes.

Initially 75 files were blocked. Forty historical ROMs were reconstructed from retained xdelta patches against the original Japanese source, and each whole-ROM hash matched its original manifest before installation as a historical test input. Rerunning the affected files recovered 65 additional passing files. Their original manifests, patches, failure/retry logs and reconstruction receipts remain preserved. These historical ROMs are not release candidates or parents for the current build.

Nine historical inputs remain unavailable. Six profiles are revoked. The other three have matching registered batch ancestry, but integrated reconstruction correctly rejects their old unsafe story-percent text. Those guards were preserved; no current ROM was substituted and no source/hash/formatting guard was relaxed. Reconstruction attempts and their rejection reasons are recorded separately. Temporary reconstruction copies were moved to approved generated storage on E: with all hashes verified, freeing the system drive; their original/new paths are recorded.

The combined-process run produced repeated Windows native Unicorn access-violation diagnostics and was stopped. Per-file isolation completed; 65 effective logs still contain native diagnostics despite normal pytest completion. This is a host/native test-engine limitation; no associated game freeze was observed in the emulator tests. Original logs remain preserved. A missing temporary-directory parent in the new runner was fixed; the nine affected files were rerun separately, with effective results recorded alongside the originals.

Two additional attempts are outside the completed-session count:

1. The older battle-menu fixture correctly rejected its prerequisite before writing: its expected Speyer fleet5 mobile pointer was zero. A separate ordinary-input probe confirmed that it remained zero at4800 and5400 while sailing continued. The identity guard was not weakened, no enemy/result was synthesized, and no victory/menu coverage was credited from that attempt.
2. A new interactive runner emitted an empty JSON-prefix line. That runner bug was corrected, and the separate readiness probe completed. This was not a game error.

The required retention preview refused a pre-existing C-path pin for `lil_opening_release_v1710/patch_reconstruction_RESEARCH_ONLY.nds`, outside the approved physical storage paths. No deletion was attempted and the safety check was not bypassed.

## Remaining gates

- Cold-boot gameplay acceptance of the Square repair, including the user's exact Raphael tutorial/crowd eligibility state.
- Closed: all ten historical test files pass using exact original test-only fixtures; revoked-profile and story-percent guards remain intact. See the follow-up report above.
- Alternate battle/duel outcomes, complete routes/late events, wireless matches and hardware remain unverified. The completed duel/victory replay supplies representative combat coverage.

Keep cosmetic changes paused while these gaps are addressed. No baseline or profile was promoted by this audit.

## Reproducible evidence

Root: `work/patch_interaction_audit_20261027/`.

- `final_audit_receipt.json`, `coverage_matrix.json`, `visual_index.json` and `sheets/`.
- `construction_write_provenance.json`: exact registered reconstruction and final byte writers.
- `resident_and_arena_proof.json`, `current_ITCM_reference_census.json`, `registered_memory_declarations.json` and `registered_source_ownership_leads.json`.
- `runtime_storage_mutations.json` and `market_cache_writer_proof.json`.
- `duel_fixture_timing.json` and `sheets/duel_victory_detail.png` bind the final prerequisite to the subsequent visible duel/result sequence.
- `isolated_tests/effective_results.json`, `summary.json`, `missing_input_classification.json`, original/retry logs.
- `legacy_fixture_recovery_results.json`, `fixture_storage_relocation.json`, `remaining_historical_profile_checks.json` and `historical_registered_reconstruction_results.json` retain historical-input recovery and refusals.
- `cases/*/capture/`: actual input schedules, journals, reports, pixels and read-only state exports.

Repeat the read-only memory check with `python -m scripts.inspect_patch_runtime_memory_20261027`. Audit runner sources are hashed in the final receipt. Preserve failed attempts and their evidence when adding coverage.
