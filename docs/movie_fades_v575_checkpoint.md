# V575: native startup movie fades and current legacy source bindings

Previous goal turn: progress, all 18 plaques compared in actual Japanese/current
UI and all 921 graphics preservation entries refreshed. Production remains
experimental V573, SHA256
`f987f1c56ba5641544e5c84698c59351e39465b15001601adddf697698d89a77`.

## Independent native color controls

Three ordinary cold boots run the original M28 startup movie for 5,000 frames,
with no inputs, battery save, savestate, gameplay cheats or movie-slot substitution.
The actual run uses the unchanged production ROM. Two isolated research ROMs
recolor only the existing English title/name coverage black or white.

Only `/FLS/M28.fls` differs in each research ROM. All other files/components,
movie table/geometry, dimensions, flags, zero/nonzero masks, palette entry zero
and every unedited texture remain exact. Each edited nonzero index maps to one;
only palette entry one is recolored. The compression slots retain their original
extents. These controls are diagnostic artifacts, not localized release candidates.

The controls independently measure where the existing English art affects the
framebuffer and how its visible color changes during fades. Neither background
color nor a nominal GPU alpha value is guessed from the actual English screenshot.

## Results

All 1,251 distinct captured frames per run are synchronized. At each capture,
pixels outside the union of 11,425 English ink/shadow points match exactly across
actual/black/white renders: 217,371,258 unowned-pixel comparisons. When the controls
show no influence, all three complete screens match. Zero-response points inside
the union also remain exact. This checks intervening blank space and surrounding
artwork, not only the foreground letters.

The colors at influenced points fit rounded black/white endpoint interpolation
at native five-bit precision within one channel step. The maximum observed error
is one. There are 2,184,114 checked color channels and 14 partially modulated captures:

`708,712,716,720,808,812,816,820,992,996,1000,1004,1008,1012`.

Both complete title planes match their production texture colors exactly:
Uncharted Waters IV at frame724 and Rota Nova at frame824. All 19 distinct progressive
Hodram-name states also have complete exact-color evidence, from frame1924 through
2000. Textures30/31 are pixel-identical and cannot be distinguished by these pixels.

Frame1004 provides a representative partial fade: all 8,378 title/subtitle coverage
points are modulated. The actual pale lettering fits the measured native response;
no stray change outside the declared English coverage is observed. The full-color
frame824 and the actual mid-fade frame were visually inspected. This is verification
of intentional fade behavior, not a new title-art repair.

The endpoint equation is a bounded color model. It does not extract internal GPU
alpha or vertex attributes, prove every blend operation, establish unsampled frames
between the four-frame captures, or verify physical hardware. No production image,
movie or ROM changes as a result of this test.

## Legacy comic/source work distinguished from new evidence

The current SLACKIMG comic block19 is byte-identical to the fully reviewed V502
block (`6f6eb664f9a61da23fb43d46549bb8d711d079f1ff4f29a22620586ff1667a25`).
The reviewed recruitment, chase, reveal, Maria and closing captions remain intact.
Selected source/current sheets were inspected again; no new defect was established
that warrants rewriting the captions or erasing ambiguous drawing details.

All eleven historically unresolved legacy blocks already have complete, reviewed
source interpretations. Current byte/extent bindings now record these explicitly:

| Source group | Interpreted images |
| --- | ---: |
| CMMN blocks0/2/3/7: portraits, goods, eight maps, items | 474 |
| SLACK13 full portraits | 42 |
| SLACK14-17 coherent portrait interpretations | 4 |
| SLACK18 landmarks | 19 |
| SLACK19 comic/sketch planes | 21 |
| Total | 560 |

All source bytes are accounted for under those prior interpretations; all except
the already localized comic block remain clean-ROM exact. This binds existing
source reviews to V573, rather than claiming another 560 newly discovered or newly
reviewed images. Native format, palette/composition and actual display relationships
remain distinct unresolved questions. The historical native-unresolved count stays
eleven. The V250 wrong-width map experiment remains superseded by the corrected
V194/V256 map interpretation. The user-approved brown marks and low-resolution
Online translation exemption remain intact.

## Artifacts

- `scripts/prepare_movie_fade_controls_v575.py` and
  `scripts/verify_movie_fades_v575.py`.
- `work/analysis/movie_fades_v575/color_control_fixtures.json`.
- `native_fade_proof.json`, `legacy_source_bindings.json`,
  `checkpoint_summary.json` and `screenshot_archive_receipt.json` in that folder.
- Actual/control capture reports and PNGs on E under
  `Generated/work/emulation_v193/movie_fades_v575_actual`, `_black`, `_white`.
- Labeled control comparison and full native frames on E under
  `Screenshots/Test fixtures/V575 Movie fades`.
- Two unaltered ordinary startup guide candidates with provenance on E under
  `Screenshots/Guide candidates/V573 Startup movie`. Publication is not approved.

Both scripts pass Ruff. All emulator and verifier processes finalized normally.
All 18 original plaque entries remain incomplete and all 22 historical requirements
retain their exact scope. The graphics goal remains active; legacy display paths,
other native contexts and source-restoration limits remain open. Revisit older
record-based checks at full completion.
