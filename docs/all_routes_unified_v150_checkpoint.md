# Experimental combined V150

V150 translates the remaining ordinary Japanese given names as **Vels** and
**Akaboo**. Vels matches established Raphael dialogue; Akaboo is the documented
phonetic project spelling, not a claimed official Latin spelling. Each complete
name fits its original twelve-byte owner. Only those two slots change over V149;
all references and the other 205 ordinary names are preserved.

## Identity and ancestry

- Candidate: `out/all_routes_combined_v150_candidate.nds`.
- ROM SHA-256: `3a1ff1f8f1734ba41c24057cee160b6b5aa2bdbc9c38dc08da8ce896dd972a8e`.
- ARM9 SHA-256: `dde53bd0a3832dc4c01437f119ba10faaaab47b053234fb27bbcab545710862a`.
- Patch: `out/all_routes_combined_v150_candidate.xdelta`, 744,024 bytes.
- Patch SHA-256: `53bba11f7acd086379c3a51596d064638a13eafcf7603f3bc9f8138914359cd1`.
- Manifest: `out/all_routes_combined_v150_candidate.manifest.json`.
- Profile: `all-routes-unified-v150`, experimental; all 435 inherited accepted
  and experimental batches in V149 order, plus every prior postprocessing stage.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Compared V149 parent SHA-256:
  `7261f62222a055b7265fe93e6afc1471926c997b792fdbe722a5d70daee950ad`.
- Clean patch input: `work/clean.nds`, SHA-256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.

The nine canonical changed paths remain `/COMMON/HELP.DK4`,
`/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
`/_pxl/personinfo.pxl`, and `/data/SC0.DK4` through `/data/SC3.DK4`.

## Verification

- All-byte ARM9/decompressed-overlay scans establish the two complete owner
  start references, with no interior or overlay matches.
- Native startup copier/BSS clear and all 207 ordinary getters preserve pointer
  identity and the other 205 names. Their outputs contain no Japanese script;
  five inherited full-width Latin initials are retained.
- Four native paired-name rows independently match complete glyph pixels and
  preserve raw-image headers, descriptors and guards. Two panels reviewed:
  leading V/A and final s/o survive without clipping or overlap.
- Four native fixed/centered fleet rasters preserve Pirate Vels/Pirate Akaboo.
- Thirty focused tests and lint pass, including source and incomplete-layout
  rejection checks plus inherited fleet/persistent-name regressions.
- Saved ARM9 matches exact research bytes; every other V149 component and all
  3,668 COMMON selections are byte-identical. Manifest hashes/order pass.
- Saved companion/Options/parenthesized-name native regressions pass. Canonical
  baseline verifier passes; the clean-ROM patch reconstructs V150 byte for byte.

Evidence: `work/analysis/residual_character_names_v150_saved_proof.json`,
`residual_character_names_v150_baseline_verification.txt`, production inputs
under `translations/residual_character_names_*` and `residual_character_names.md`.

## Remaining full goal and gameplay

Cold-boot title/New Game/character selection, established story/town, Vels's
story name, Akaboo's town presentation, paired-name views and fleet views.
Inspect full leading/final letters; retain all inherited item/crew/map/Options/
Deck/save/help/sound/tribute/caption/race checks. Native actor/scene eligibility,
clear/initialization contracts, other name consumers and physical composition
remain open. Canonical promotion requires explicit user acceptance.

Zero Japanese given-name results does not prove source-faithful older English.
The fresh saved-ROM audit `work/analysis/given_name_fidelity_v150.json` records
all 207 clean/current labels and twelve concrete review leads: governor
abbreviation, senior-monk rank, couple qualifiers, alluring/mysterious/collapsed/
suspicious descriptions, Dandy/Dundee and Sakura/Cherry. Unflagged labels also
need exhaustive semantic review. Five full-width Latin initials remain a
formatting/fidelity audit item.

Remaining COMMON stays at 245 Japanese selections/133 physical records (31
promotional, 214 scene/artwork/name copies). Remaining ARM9/UI/graphics and
older-English fidelity are still in the active goal. No full goal completion,
canonical acceptance or new commit/push is claimed. After completion, revisit
older record-based checks as requested.
