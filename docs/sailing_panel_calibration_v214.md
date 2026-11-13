# Sailing panel native calibration and English layouts V214

2026-10-07. Previous turn confirmed three live Japanese panels and reviewed their
English. This turn executes the original producer and prepares complete readable
English layouts. **V211 is unchanged; native English integration remains pending.**

## Native producer execution

The original ARM9/autoload code, declared overlay at `01FFA000` and complete
73,480-byte Kanji font are loaded. The font's actual runtime pointer comes from
the native literal at D19B8. No glyph-map or painter call is substituted.

All three original strings execute `01FFB4BC` completely:

| Panel | Source character pairs | Last nonzero output offset |
|---|---:|---:|
| Info | 70 | 6377 |
| Search | 152 | 14281 |
| Declare War | 128 | 11753 |

Every observed native lookup equals the corresponding complete source CP932 pair,
in order. Complete returns, stack and outer buffer guards pass. The zero target and
64 KiB outer capacity are explicit calibration fixtures; font disk loading is not
executed. Observed nonzero writes fit within the caller's `3800`-byte uploaded span.
This does not yet establish its physical tile/sprite arrangement or English output.

The pair parser is incompatible with an assumed plain-ASCII overwrite. It also
produces a packed sprite stream with metadata, rather than an interchangeable
linear 256×192 bitmap. Preserve that contract when adding English production.

## Complete proposed English layouts

The actual six-by-eleven ASCII font from V211 supplies every complete glyph.
Bodies are single logical paragraphs, automatically word-wrapped at 40 columns.
The formatter verifies that joining the rows reproduces the complete prose.
Heading centering, every first/last letter and blank cell, row bounds and the
reserved footer region are checked in the proposed canvas.

Info uses two body rows; Search and Declare War use five each. All three previews
were visually reviewed. Their headings and complete instructions are readable
without footer overlap or dropped words. No lore/rule is shortened to satisfy the
old source allocation. The font, manuscript and pixel hashes are saved.

These are proposed 256×192 source layouts, **not** proven native-packed assets or
an English ROM. The physical packing/callback, caller ABI/pool ownership and live
English mode captures remain required before setting the formatting/native-display
gates or registering a layer. Neither plain ASCII nor a linear preview may be
copied into the original packed producer blindly.

## Artifacts and next action

- `scripts/calibrate_sailing_panel_overlay_v214.py` and
  `work/analysis/sailing_panel_overlay_v214/calibration.json` plus full output buffers.
- `scripts/prepare_sailing_panel_layouts_v214.py`, `English_layouts.json` and three
  complete English PNGs in the same directory.
- Reviewed source/context/English: `translations/sailing_mode_panels_manuscript_v1.json`.

Focused Ruff passes. Next: recover the packed stream's display mapping against the
confirmed Japanese captures, implement bounded English production with complete
ABI/source protection, then cold-boot and integrate all three panels. The entire
graphics goal, four Online bodies and other remaining name/raw/native/gameplay
work stay open. No goal completion or candidate promotion is implied.
