# Combined V159: complete item text presentation

V159 is the latest **experimental** combined candidate. It has not been
promoted to the canonical baseline. The full translation goal remains incomplete.

## What changed

34 visible source-reviewed natural-English records cover item headings, all
13 categories and all 16 crew roles. A separate `Use` reference is preserved;
its native branch does not draw a heading, so it receives no visible translation
or formatting credit. Existing English descriptions retain their complete words.
The compiler supplies whole-word rows for all 218 actual item slots.

Private item presentation getters leave the global category/role tables intact.
Separated columns prevent category, role, effect and number overlap. The native
single-line painter receives every compiled paragraph row. Two complete parent
rows previously ended at screen x296; four source-locked position fields now
place them at x8/y64 and x8/y80, below the icon. All seven native crop requests
fit and preserve every complete glyph cell and pixel.

Full promotional initialization exposed generated map slots 198–217, beyond the
displayed collection total of 198. A single-terminated COMMON string could feed
garbage continuations into the new multiline helper. The complete projection now
covers all 218 slots and double-terminates those map paragraphs. COMMON itself
is unchanged from V158. Executable pool loading now uses the game's SDK cache
maintenance sequence and reserves the full 20576-byte main pool.

## Verification and its scope

The earlier 2090 local rasters, 12 Advice-menu cases, 456 crew-owner cases and
280 ship-owner cases retain their actual research hashes. They are not relabeled
as newly executed V159 cases. Deterministic source-locked transforms preserve
their complete text and helpers while changing the explicitly mapped parent,
table range and cache wrapper. Their reviewed evidence is locked by the release.

Fresh execution on the final ARM9 checks:

- 320 generated-map rasters and 20 static/default regressions in both item
  screens and pixel formats; all ten regenerated panels match reviewed hashes.
- 37 complete promotional initializers / 1110 names, all 218 metadata
  initializers, 257 lookup ABI cases, startup/caches/ARM7, arenas, counter storage
  and native parent crops.
- 408 equipment-role rasters: all 28 ordinary role-dependent item resources,
  every role label, all three accessory slots and seven controlled membership,
  duty and fleet-leader states. Native eligibility preserves full owner names
  in both allowed and denied states using the original styles 1 and 4.
  All eight additional panels were reviewed.
- Inherited 14 Gallery and 64 duel rasters, 24 movement callers, 54 village
  callers, nine monthly scope cases, 207 ordinary names, 239 shared name owners,
  two sailing-status rasters, 3668 COMMON selections and 704 copy-alignment cases.
- 73 focused tests, including rejection of lost leading letters, missing reviews,
  wrong owner styles, clipped rows, stale proof, skipped eligibility and absent
  cache maintenance. Changed implementation/verification files pass Ruff.

The saved ROM matches the exact verified ARM9 target. All 435 profile batches,
accepted layers, prior terminal-stage metadata and changed-record lineage are
preserved. Canonical menu/graphics invariants and exact clean-ROM patch
reconstruction pass. Only ARM9 differs from V158.

Controlled state, artwork, backgrounds, palette appearance, physical GPU/controller
behavior and downloaded saves are still outside these native text proofs. The
inherited FE panel repair stays exact in the relevant code/data; its full earlier
1061-case matrix was not rerun. No full-game guarantee is claimed.

## Candidate and lineage

| Artifact | SHA-256 |
| --- | --- |
| Canonical base: `out/raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base: `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| V159: `out/all_routes_combined_v159_candidate.nds` | `51a89ca2cf0ec6beab6e2a68670eb1cc6368d069fee1947fe5fc367a644d83a5` |
| V159 ARM9 | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Registry at V159 build | `ccdd4c0d7b4c4134f8f8aff42a24a4efd608992f9eb0e2833830401d0e548655` |
| V159 patch: 760016 bytes | `4f1079a3568d3830eb1e4e180b87a7de7d3aabd9e447ba0ce7f1ca68fdbc7cb9` |

Registered profile: `all-routes-unified-v159`, experimental. Its 435 experimental
profile batches and all V158 terminal stages precede the new item stage. All
accepted layers are already baked into the canonical baseline; zero additional
accepted batches are required. The exact registry hash, full batch list, changed
records and verification results are in the adjacent `.manifest.json` and
`work/analysis/item_v159_saved_proof.json`.

Compared with the canonical baseline, the nine changed internal paths remain:
`/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`, `/__arm9__.bin`,
`/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`, `/data/SC0.DK4`,
`/data/SC1.DK4`, `/data/SC2.DK4` and `/data/SC3.DK4`.

Physical cold-boot testing must cover title, New Game captain selection, an
established story scene, town UI and changed item/Advice/Gallery screens,
including crew/ship owners, denied role equipment and generated maps. Do not
load a savestate for acceptance. Explicit user acceptance is required before
canonical promotion. No commit or push is claimed at this checkpoint.

## Full goal remaining

245 COMMON selections / 133 physical owners still need their actual consumers
and layout integration. Further ARM9/UI consumers, Japanese graphics, name
fidelity, Reports/Sailing Help persistence, BGM physical audio/input and complete
gameplay checks remain. Rough byte/pointer inventory counts are leads, not
untranslated-message counts. Final packaging/progress and GitHub commit/push
remain campaign tasks. On completion, revisit the older record-based checks.
