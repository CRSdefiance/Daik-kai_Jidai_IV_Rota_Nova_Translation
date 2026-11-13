# V447 source-faithful sea and sailor data Help

Status: experimental; full graphics goal active. All22 historical requirements
and all18 incomplete plaque entries remain in the audit.

## Source findings and localization

All18 plaque translations remain supported by their original meanings. The
associated Help articles were not complete: articles153–180 included `see below`,
generic descriptions and unrelated equipment advice. This release restores all28
articles from clean Japanese, with source neighbors, glosses, context, individual
five-gate reviews and natural American English in
`translations/sailor_data_help_manuscript_v1.json`.

The restored facts include food/water barrel counts, zero-crew Game Over, fatigue100
causing crew loss and possible mutiny; all six Mood and physical Health states;
recovery through appropriate rooms and Doctor-used medicine; every attribute and
skill's meaning, relevant jobs and related attributes; gradual HP recovery and
the zero-HP Dying state; and selecting empty/occupied equipment slots to equip or
remove an item. Original links and their order are preserved.

The current Health skill is the source vitality value, indicating maximum HP and
physical resilience. Its article distinguishes this skill from the Health plaque's
current physical condition. Mood is also distinguished from the Spirit attribute.
No plaque is marked fully completed, and no graphic is renamed in this release.

## Formatting and actual testing

The compiler lays out29 pages for28 articles. HP and Health has one automatically
created continuation, ID208; no source facts are cut to fit a single page. All208
existing IDs, sentinel203 and all180 unselected articles remain exact. The archive
now has209 topics, all of which pass complete native loading and guard checks.

All29 native previews were visually reviewed. Actual normal New Game Help
navigation verifies all29 full-glyph pages and all54 original link widgets,
including complete first and last letters. HP's continuation/return restores the
whole page exactly. Native L/R history returns exact pixels. All57 earlier title,
New Game, story, town and Help-entry captures match V440.

The first navigation attempt was diagnosed from actual widget history: tapping an
already selected first link activates it immediately, so a following A enters its
first child. Those attempted changed-page captures are excluded. The corrected
normal-input replay uses A alone for the already selected first child. No ROM
defect is inferred from that navigation error.

Tests are targeted automated DeSmuME runs, not hardware testing, complete routes
or actual gameplay proof of every described stat formula/condition. Twenty-eight
remaining legacy Help marker matches are listed in the proof for source review;
matching a marker alone does not establish all missing facts.

## Handoff

Candidate: `all_routes_combined_v447_candidate.nds`

SHA-256: `74ece5ca2e9f4c40de9ccb57d76af7b2d7b83fd114c012be0941cf314dd0e1f6`

Patch SHA-256: `c8832110adf5fd92357e7f5180af7f20765b7828e25131c350ab6a81c7e45048`

Profile: `all-routes-unified-v447`, all470 inherited batches and all V443 stages,
plus `translations/sailor_data_help_release_v1.json`. Only `/COMMON/HELP.DK4`
differs from V443; every other internal file/component, including all artwork,
ARM9 and the prior Guild repair, is byte exact. Clean patch reconstruction passes.

Canonical base remains `out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
No promotion is made. User cold-boot testing should cover title/New Game/opening,
town UI and Help → Data Guide → Sea Info / Sailor Info, including HP continuation.

Verifiers: `verify_sailor_data_help_release_v447.py`,
`verify_sailor_data_help_live_v447.py`, plus209 native archive loads through
`verify_help_archive_v281.py`. Targeted Ruff passes.
Proof: `work/analysis/sailor_data_help_release_v447/release_proof.json`.
Actual report: `work/emulation_v193/sailor_data_help_fixed_v447/capture_report.json`.

ROM, exact patch, manifest and three verified guide screenshots are published to
`E:\Rota Nova translations`. Occupied Weapon/Armor, regional/legacy/Gallery/ending
contexts and all ongoing plaque gates remain open. Revisit older record-based
checks at true full-goal completion.
