# Combined graphics checkpoint V217

## Candidate and ancestry

Experimental profile: `all-routes-unified-v217`.

- ROM: `out/all_routes_combined_v217_candidate.nds`.
- SHA-256: `124588d04ad361b505e1eccb1b05aa422ad5e919771d1faf4be256cd734b713e`.
- Patch: `out/all_routes_combined_v217_candidate.xdelta`.
- Patch SHA-256: `e7e767f3c6a16ae929d8b1c972cd773220ef2fcf52a56c014da05a36545d002b`.
- Canonical parent: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Patch source: `work/clean.nds`, SHA-256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.

All 467 V211 batches, 114 baked accepted layers and inherited terminal stages are
retained. The registered builder reproduces V211 exactly after its extension.
Every existing internal file, ARM7 and the original overlay remain identical to
V211. Only ARM9 changes: four scoped producer calls, existing mode sprite arguments,
and the source-locked staged graphics pool/cache/arena extension. Applying the
patch to the clean ROM reconstructs every byte of V217.

## Complete English instructions

**Info Mode:** View information about the cities and ships on screen. Select a target.

**Search Mode:** Press A to search. You may find water, food, items, or other supplies.
If you find nothing, sailor fatigue rises by 3. Sailors may desert or be attacked
by wild animals while searching.

**Declare War Mode:** Select a fleet or city on screen to begin a battle. Declaring
war puts you at war with that faction and greatly lowers goodwill. You cannot
declare war on an allied faction's fleets.

The manuscript contains complete logical paragraphs. Automatic forty-column
wrapping uses the original six-by-eleven English font, with two/five/five body
rows. No source instruction is removed to satisfy the old Japanese allocations.
The exact fatigue penalty and fleet-specific alliance restriction are preserved.

## Native encoding and protection

The original CP932 producer remains intact. Only the sailing-specific calls select
prepacked English assets; an unknown source pointer follows the original producer.
The font, palettes, Japanese source fields and unrelated native code stay intact.

The replacement uses the verified consecutive 32x16 four-bit sprite banks. The
heading occupies six banks centered at (32,2). Each body row starts at (8,32+16*n)
and requests eight banks; all ink remains within x=8..247 and above the footer.
Unused upload bytes are explicitly cleared to prevent earlier-mode text lingering.
There is no linear-bitmap overwrite, guessed CP932 encoding or manual prose padding.

Four producer paths pass complete buffer/guard/stack checks. Actual parent fragments
and their native bank loops pass for Info, Search, and Declare War with and without
a selected target: 180,224 foreground/blank pixels across four variants. The sprite
submission is an explicit bridge in that fixture, not a GPU claim. Native autoload,
ARM7 source preservation, complete staged copy and cache maintenance pass; the
expanded main arena reserves the full pool and preserves every other bound.

## V216 failure and correction

V216 is revoked. Its ordinary cold boot showed English Search/Declare War, but the
first Info display remained Japanese. Initialization calls the producer at
`02070284` using a second, byte-identical Info string at `02147828`; mode cycling
uses `02147778`. V217 covers both exact sources and the initialization call.

The mode literal addresses also correct an earlier analysis label: mode 2 loads
Search through literal `0206F418` and calls at `0206F178`; mode 1 loads Declare War
through `0206F420` and calls at `0206F200`. The two target-selection display states
belong to Declare War, not Search. This is recorded from the actual LDR addresses.

## Cold-boot verification

The final V217 ordinary cold boot passed all four mode captures. Complete foreground
and blank masks match in 180,224 pixels, including all 5,496 English ink pixels.
Every leading/trailing letter and punctuation mark is complete. All four panels
and the title menu, New Game, established story and town were visually reviewed.
See `work/emulation_v193/sailing_panels_v217/capture_report.json` and
`work/analysis/sailing_panels_v217/live_pixels.json` for the hash-pinned evidence. The ordinary input
schedule tests first-opening Info at 17400, Search at 17900, Declare War at 18400,
and cycling back to Info at 18900, without savestates or RAM injection.

## Remaining scope

The separate no-attack-target notice still displays Japanese. Both its ordinary
string and packed graphics source are mapped, and the complete English
"There are no targets to attack." is reviewed in
`translations/sailing_no_attack_target_manuscript_v1.json`. Its native formatting
and integration remain pending; it is not silently counted as part of these panels.

The four incomplete Online screenshot bodies/chat, confirmed-name consistency,
unclassified raw/embedded consumers, contextual artwork/display checks and final
whole-scope gameplay audit remain open. This candidate is experimental and has not
been promoted. The full graphics goal remains active. At completion, revisit the
older record-based checks as requested.

## Reproducible verification

- `dk4tool/patch/sailing_panel_graphics.py`.
- `translations/sailing_panel_graphics_release_v2.json`.
- `scripts/verify_sailing_panels_v217.py`: original producer fallback, four native
  producer paths, four parent layouts, startup/cache/ARM7 and arena checks.
- `scripts/verify_sailing_panels_live_v217.py`: complete glyph/blank masks from play.
- `translations/sailing_mode_panels_native_review_v217.json`: final five gates and
  native English display review; the source manuscript is the immutable pre-build snapshot.
- `scripts/verify_sailing_panels_release_v217.py`: exact stack and patch verification.
- `work/analysis/sailing_panels_v217/native_proof.json` and `saved_proof.json`.

Focused Ruff checks pass. Emulator verification does not claim physical DS testing
or human acceptance of this candidate.
