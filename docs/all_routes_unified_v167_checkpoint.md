# Combined V167: Flagship and Fill Evenly

V167 is the latest **experimental** combined candidate. Two further shared
button labels now have complete natural English in both atlas copies. All ten
V166 labels, other translations, code and repair stages remain exact. The full
goal is incomplete; canonical promotion and final commit/push remain pending.

## Source meaning corrected and confirmed

| Japanese | English button | Meaning/context | Lettering rectangle |
| --- | --- | --- | --- |
| 旗艦重視 | Flagship | Crew preset that gives the flagship priority. | `[91,162,133,173]` |
| 均等補給 | Fill Evenly | Even replenishment; original Help describes filling water and food evenly. | `[91,178,133,189]` |

Earlier research/checkpoint prose misread the first source as square-sail
priority. The full-resolution graphic says **旗艦重視**, and original Japanese
Help independently says **［旗艦重視］旗艦へ優先的に配置。**: assign sailors to
the flagship first. The earlier wrong interpretation was never rendered into a
candidate; that button remained Japanese until this correction. Flagship is the
complete name of the priority preset, in the crew-allocation context.

The original departure-office Help says Yes fills water and food evenly to the
maximum; No allows changing their ratio. This supports Fill Evenly's meaning.
The exact actual contexts of this shared supply sprite still need native mapping;
it is not classified as another crew-allocation button merely by atlas position.
Source Help entries, byte bounds and hash are recorded in
`work/qa/frame_buttons_v167/source_context.json` and the native report.

Flagship uses the existing fixed five-pixel advance, occupying 40 of the
original 42 available pixels. Fill Evenly uses all original native glyph ink
with blank side bearings removed: one blank column between letters and three
between words. Its complete allocation is 41 pixels. Only the native font's two
proven blank leading rows are trimmed. No visible glyph pixel is resized,
cropped or removed; the word separator and first/final letters remain intact.

The bitmap builder's optional `glyph_spacing: native-ink-v1` applies only to this
new baked label. Every older fixed label retains its existing geometry. This is
an offline graphic feature; the game's runtime text/font code is unchanged.
The modified registered builder reproduces **the complete V166 ROM byte-for-byte**.
Evidence: `work/analysis/v166_spacing_builder_reproduction.json`.

## Graphics preservation and reviewed previews

The source is immutable canonical `/_pxl/__frame.pxl`, 256×256, four-bit PXL,
matching clean Japanese exactly. White faces and dark shadows are erased only
inside the two new rectangles, reconstructing owned background pixels from
nearest original row colors. Every earlier English pixel, border, other
lettering/art, header, palette and encoded extent remains exact versus V166.

`/GRP/CMMNIMG.DK4` block 5's matching right half is synchronized. Its entire
left half, all 83 palette banks, block header/flags, other archive blocks and
extent remain exact. Only the two new lettering rectangles differ from V166.
Both complete source/English atlases, enlarged buttons and the complete embedded
bank-zero storage view were reviewed. Native bank selection and alpha remain
unproved. Upper frame/calendar/trade labels and embedded left-half Japanese remain.

Previews: `work/qa/frame_buttons_v167/review.png` and
`work/qa/frame_buttons_v167/english_embedded_bank_zero.png`.
Artwork: `work/analysis/frame_buttons_v167_artwork.json`.

## Native glyph evidence and its limits

**95 focused graphics tests pass**: ten new preset/spacing tests and all 85
earlier graphics tests. New checks reject missing first and final characters,
verify full native glyph ink and the word space, preserve all ten previous
records/pixels, reject unknown spacing/overflow/cropped source glyphs, check
the complete profile/stages, and pin the original Help meaning. Builder, new
script and tests pass Ruff.

The native font lookup and bitmap draw routines `020D1820`/`020D16B4` execute
full eleven-row cells in the **actual source 256×256 four-bit PXL geometry**.
Fixed labels execute together. Each proportional letter, including the space,
executes separately in a blank image with the original header/palette; its
complete native output matches independent original font masks. Complete native
ink is then composed offline and compared with every packed English pixel.
Saved registers, stack, header/palette and memory canaries pass.

A rejected research probe showed why this distinction matters: the original
four-bit font routine clears all six columns of a glyph cell, including blank
side bearings. Sequential overlapping cells would erase 23 earlier ink pixels.
Those pixels are all present in the final baked bitmap. The rejection is saved
at `work/analysis/frame_v167_sequential_spacing_rejection.json`; no release ROM
was modified by that probe. The passing proof verifies complete native shapes
and final offline composition, **not a live proportional text renderer**.

Common image sizing confirms 256×256 under controlled loaded resource/header
and selector inputs. Embedded synchronization proves exact pixel storage, not
actual loader/bank selection. Actual loose/embedded loading, all live crops/
contexts, parent/GPU palette/alpha, controller behavior and physical gameplay
remain pending. These scoped checks do not clear every screen in the game.
Native evidence: `work/analysis/frame_buttons_v167_native.json`.

Saved verification preserves all inherited components/resources, terminal
stages, relocations and changed-record IDs. ARM9, COMMON/HELP, all routes and
every other graphic remain byte-identical to V166. Canonical menu checks,
complete prior-ROM builder reproduction and exact clean-ROM patch reconstruction
pass. Saved proof: `work/analysis/frame_v167_saved_proof.json`.

## Candidate and lineage

| Artifact | SHA-256 |
| --- | --- |
| Canonical base: `out/raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base: `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| V166 comparison and exact builder reproduction | `d53b7d22c913bf862f10f09b4a456326950173870887732bf2eb17c61c415ee5` |
| V167: `out/all_routes_combined_v167_candidate.nds` | `7ac37ac46a36c21bb753af83b0db05d5cb9adb94cf9f5b12c07c4701bf2bccec` |
| ARM9, exact V166 | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Registry at V167 build | `2b47a005243975b1431995bfb8039a9aa267daecf2d235ae589aa7c503a0800e` |
| Registered builder | `8e7d7891ebbcefe6843a77e33d57766de411ffa77f82301a6d7955f5dd83dc5e` |
| V167 patch: `out/all_routes_combined_v167_candidate.xdelta`, 773066 bytes | `24f8a0fa7427019accff1ddf9dad0edcc940c0921c288739707f592d12cb965b` |

Profile: `all-routes-unified-v167`, experimental. The integrated builder uses
the immutable canonical base and every inherited terminal stage. All 450
non-frame V166 batches are unchanged. Two expanded canonical batches explicitly
supersede their earlier versions, preserving every previous record:

- `translations/frame_action_buttons_graphics_v3.json` supersedes v2, with ten
  exact prior records plus Flagship and Fill Evenly (12 labels total).
- `translations/frame_action_buttons_cmmnimg_sync_v3.json` supersedes v2, keeping
  its original archive/block locks and record ID while synchronizing the expansion.

Older batches/profiles remain reproducibility records. There are **452** current
batches. Accepted layers are baked into canonical; zero additional accepted
batches are required. The adjacent
`out/all_routes_combined_v167_candidate.manifest.json` records the full stack,
baseline/registry identity, changed files/records and build checks.

Compared with V166, **only `/_pxl/__frame.pxl` and `/GRP/CMMNIMG.DK4` differ**.
The canonical changed path set remains 25:
`/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`, `/GRP/CMMNIMG.DK4`,
`/GRP/SLACKIMG.DK4`, `/Iseki/dock.pxl`, `/__arm9__.bin`, `/_pxl/__frame.pxl`,
`/_pxl/deck04.pxl`, `/_pxl/dividecrewinfo.pxl`,
`/_pxl/mysterymap/mys_hunt_d.pxl`, `/_pxl/personinfo.pxl`,
`/_pxl/slackimg12.pxl`, `/_pxl/slackimg20.pxl`,
`/data/SC0.DK4`, `/data/SC1.DK4`, `/data/SC2.DK4`, `/data/SC3.DK4`,
`/evstill/evstill168.pxl`, `/evstill/evstill169.pxl`,
`/evstill/evstill170.pxl`, `/evstill/evstill171.pxl`,
`/evstill/evstill206.pxl`, `/evstill/evstill207.pxl`,
`/evstill/evstill208.pxl`, `/evstill/evstill209.pxl`.

Before acceptance, cold-boot without a savestate. Check title/New Game,
captain selection/name entry, an established story, town UI and all inherited
item/Advice/Gallery/treasure/fleet/village/button/score screens. Check the
Flagship crew preset and every Fill Evenly supply context for complete words,
word spacing, crops, borders, palette/alpha, controller behavior and actual
allocation/replenishment effect. Recheck the ten earlier frame labels. Explicit
user acceptance is required before canonical promotion.

## Full goal remaining

COMMON remains 245 Japanese selections / 133 physical owners needing actual
consumer/layout integration. Other ARM9/UI and name/source fidelity, Reports/
Sailing Help persistence, BGM physical audio/input, downloaded states and full
gameplay checks remain. The historical graphics inventory still has **13**
resources with other Japanese lettering: upper frame/calendar/trade/selection
labels remain, along with marker gender symbols, title artwork, online screenshot
lettering, FLS logos, CMMNIMG left-half/remaining frame labels, the embedded title
copy and unclassified art. Actual graphic consumers/crops and image 207's clipped
source mark still need review. Final packaging/progress, canonical acceptance
and GitHub commit/push remain. On full goal completion, retain the requested
note to revisit older record-based checks.
