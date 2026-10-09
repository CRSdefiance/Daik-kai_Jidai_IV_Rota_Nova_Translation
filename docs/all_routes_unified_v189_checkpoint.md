# V189 Online screenshot headers and resource registration

2026-10-05. Graphics goal active/incomplete. Four readable phrases were translated
from the exact canonical Japanese screenshots, using natural English and preserving
original header/palette/dimensions/decorative borders/unowned pixels. This is partial
screenshot localization: body UI, status/player labels, dialogue and chat remain pending.
No uncertain Online31 dialogue transcript is shipped.

## Source and editorial review

| Resource | Japanese | English |
| --- | --- | --- |
| Online24 heading | 人物情報 | Profile |
| Online24 description | あなたの情報です | Your character information. |
| Online33 heading | クエスト情報 | Quest Info |
| Online33 description | クエスト情報を表示します | View quest information. |

Profile is a natural character-information tab label. Its description explicitly
identifies the player's character. Quest Info uses a conventional English UI
abbreviation. Every record has source/context/localization/naturalness/formatting
review, source meaning, localization note and complete glyph raster hashes.

Letters are rendered whole at 5/6px, with antialias shading projected into the
unchanged original palette. First/last letters and terminal periods have visible
native palette ink; eight probes removing their actual glyph regions are rejected.
Original Japanese is cleared only inside owned header text rectangles, filled from
text-free same-row donor columns. The covered background is estimated, not claimed
recovered. The original/English header sheets were inspected at 2x/4x; live native
readability is still unverified. No generic placeholders or guessed chat are inserted.

## Actual Online resource selection

The unchanged native static initializer at `0x02111A90` executes 449 distinct
instructions and returns with preserved stack/register ABI. Its real global owners
contain original ROM filenames; owners are not substituted with a supplied table.
The four real category descriptors at offsets `12F88C`, `12F898`, `12F8A4`, `12F8B0`
select 13 pages and 23 screenshot selections.
The actual parent at `0x02104744–0x0210477C` selects a screenshot from the page's
native table and calls `0x020D3D30` with origin zero and extent 256x192.
All selected screenshot resources have this exact native extent.

Indices below are zero based; category names are not inferred.

| Resource | Category | Page | Screenshot | Actual native owner |
| --- | --- | --- | --- | --- |
| `/_pxl/online/Online24.pxl` | 0 | 2 | 1 | `0x02386B50` |
| `/_pxl/online/Online27.pxl` | 1 | 2 | 0 | `0x02386B78` |
| `/_pxl/online/Online31.pxl` | 2 | 0 | 1 | `0x02386BDC` |
| `/_pxl/online/Online33.pxl` | 2 | 1 | 0 | `0x02386C40` |

Evidence: `work/analysis/online_resource_pages_v189.json` and
`scripts/probe_online_resource_pages_v189.py`. Registration, resource selection and
declared extent are proved. Filesystem loading, navigation/input, layer transforms,
GPU/palette composition and live readability remain open. This is stronger than the
older supplied-owner crop probes, but is not gameplay evidence.

## Required handoff

- Candidate: `out\all_routes_combined_v189_candidate.nds`
- SHA-256: `0361d5ab8d08b2493c1dfd1bb495b1ffbe42126da51b4296771582c0ceae1e74`
- Canonical base: `out\raphael_natural_v2_accepted_base.nds`
- Canonical SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Profile: `all-routes-unified-v189`; experimental, no canonical promotion.
- Accepted layers: baked into canonical base; 0 additional accepted batches applied.
- Experimental batches: 465; every V188 batch, record ID and terminal stage retained.
- Changed versus V188: `/_pxl/online/Online24.pxl`, `/_pxl/online/Online33.pxl` only.
- All 36 changed paths versus canonical are listed in the manifest.
- ARM9 unchanged versus V188: `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf`.
- Patch: `out\all_routes_combined_v189_candidate.xdelta`
- Patch SHA-256: `13885f1d7a8d789a5bc26e1d6fa9a3b2235a2a98b6789b1ea9f9f66cf17957ad`
- Clean patch base: `work/clean.nds`, SHA-256 `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.
- Verification: final saved-artwork identities, palette/header/extent/border/unowned
  preservation, complete glyph raster coverage, eight actual first/last-glyph removal
  probes, full exact V188 reproduction, complete manifest/batch/record/terminal-stage
  inheritance, golden menus, unchanged unrelated files, Ruff and exact patch reconstruction.
- Cold-boot review remains required: unfaded opening/video logo, title menu, New Game
  selection, established story scene, town UI and the changed Online24/33 Extras pages.
  Do not load savestates. Actual input/navigation remains unverified.

## Artifacts and remaining work

- `translations/online24_headers_art_v1.json`, `online33_headers_art_v1.json`
- `scripts/online_headers_v189.py`, `probe_online_resource_pages_v189.py`
- `work/qa/online_headers_v189/Online24_header_review.png`, `Online33_header_review.png`
- `work/analysis/online_headers_v189_saved_proof.json`
- `work/analysis/v188_online_headers_reproduction.nds` (exact V188)
- `translations/graphics_completion_campaign_v1.json`

Four historical Online files still require full localization, including Online27
chat/status and Online31 dialogue. The historical inventory remains 921 screened,
26 confirmed, 22 localized including partial/unresolved source marks, four unfinished;
these counts do not prove full pixel/native clearance. Unclassified embedded/contextual
art, retained brown water marks, clipped image207 interpretation, Latin name-card
fidelity, full-resolution source reviews and broad live/gameplay/final acceptance gates
remain. Keep the user's older record-based-check follow-up for eventual full completion.
