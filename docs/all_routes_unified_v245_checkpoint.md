# Combined V245: six incomplete inherited menu bitmap captions repaired

V245 is **experimental**. The full graphics goal remains active. The previous turn
made progress on additional exact screenshot source research. This turn maps six
real radial-menu views, finds a stored-art defect and corrects both marker copies.

## Source defect and full-family correction

The six inherited English menu bitmaps in the immutable canonical baseline were
small, distorted replacements with white fragments of the original Japanese still
present underneath. The original and inherited images were compared at integer
enlargement. This defect predates the current graphics campaign; the canonical
baseline is preserved, and the correction is layered through the registry.

| Original Japanese | Retained natural English | Source cell |
|---|---|---|
| 機能 | Functions | `(0,0),64×24` |
| 水夫編成 | Crew Setup | `(0,24),64×24` |
| 甲板画面 | Deck View | `(0,48),64×24` |
| 情報 | Info | `(0,72),64×24` |
| 航路図 | Route Map | `(0,96),64×24` |
| アイテム | Items | `(0,120),64×24` |

Every cell's whole lettering area, relative`[3,2,61,18]`, is restored before full
native-font English is drawn. Original Japanese ink extends to row16, which the
older replacement did not completely clear. The new area contains only the reviewed
English foreground; all first/last letters, word spaces and bounds pass. Native
five-pixel spacing retains every source glyph pixel without trimming visible ink.

The six clean Japanese cells share the same background throughout the lettering
area. **927 of928 coordinates per cell** have exact agreeing visible background
references in another original cell. The one coordinate `(23,11)` is concealed by
all six captions. Its index6 is reconstructed from thirteen visible samples on the
same continuous diagonal stripe. This one pixel per plate is explicitly an
inference, not a recovered original pixel. All original cell borders, including
their differing lower bevel pixels, are outside the repaired area and remain exact.

The repair applies to `/_pxl/__marker.pxl` and its synchronized left-half copy in
`/GRP/CMMNIMG.DK4` block5. The complete right-half frame, both gender cells, every
other marker caption, all83 palette banks, headers, extents and other archive
blocks remain exact. Neither ARM9 nor any renderer/formatter rule changes.

## Real native views and cold boot

The saved normal-gameplay RAM identifies six real initialized marker views, with
all six source origins above and64×24 extents. Their owner is`02313F74`. The original
nonvirtual resolver at`020D4170` resolves each actual view to the complete saved
35,444-byte marker resource. All six cases preserve the view and native stack/saved
register ABI;212,664 returned resource bytes are verified. The low byte of the
palette parameter is10. Its higher padding bytes can contain old heap data and
are not interpreted as a palette index.

A virtual method at slot+16 was initially suspected as an image getter. Its code
does not support that interpretation; it is neither used nor presented as getter
evidence. Resolution uses the already mapped original`020D4170` method instead.
The snapshot CPU replay is separate from physical framebuffer observation.

A new V245 cold boot replays ordinary Lil opening, Amsterdam, Crew Setup,
confirmation and all six selected radial-menu states. Eight complete live caption
masks, including Yes/No, pass. Twelve earlier full screenshots match V241 exactly.
The six selected menu screenshots also remain identical to V241. Thus the stored
art correction introduces no visible regression in this observed DS path. This
does not globally establish why the baked caption area differs from the live text,
nor clear all alternate consumers or every palette/alpha composition.

The core is pinned DeSmuME git95b4d79, native256×384 software rendering, interpreter,
one core and English firmware. No savestate, RAM injection or fixture ROM is used.
All captured PNG/core/ROM identities and empty callback-error lists pass. The final
RAM export is read-only; all emulator/build processes are terminal.

## Registered integration and exact patch

The initial registration was rejected because the builder allows one native-label
batch per PXL. The corrected profile explicitly supersedes the old gender batch
with a merged version that preserves its two compact records and adds the six
repairs. Its marker synchronization explicitly supersedes the prior sync. All
**467** complete batches, earlier record IDs, required layers and terminal stages
are retained; no shared builder change or historical hash bypass was needed.

| Artifact | Identity |
|---|---|
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Canonical SHA-256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Candidate | `out/all_routes_combined_v245_candidate.nds` |
| Candidate SHA-256 | `57b7f42f04f60c5e6f06d03ebe91eacbaff04204dde27967fd3e3b205634d3c4` |
| Profile | `all-routes-unified-v245`, experimental |
| Exact clean-ROM patch | `out/all_routes_combined_v245_candidate.xdelta` |
| Patch SHA-256 | `3503984bbfcc34df11ccca3ecca4b3db66f2f8da41508f2c2c5562161c3fbc68` |
| Manifest | `out/all_routes_combined_v245_candidate.manifest.json` |

Only the marker PXL and CMMNIMG archive change relative to V241. Every other
internal file, ARM9 and ARM7 remains identical. The patch is applied to the pinned
clean ROM and reconstructs V245 byte for byte. No canonical promotion is performed;
user cold-boot acceptance remains pending. The specific observed menu path is Lil
opening → Amsterdam → X/Menu and its six entries.

## Evidence and remaining work

- `scripts/prepare_radial_marker_v245.py`: canonical/source locks, background
  references, full native-font repair and exact expected marker bytes.
- `scripts/verify_radial_marker_release_v245.py`: every complete new glyph mask,
  ownership/bank/header/copy preservation, inherited stack and exact patch.
- `scripts/verify_radial_marker_live_v245.py`: eight live words, earlier frames and
  six real native cached views. All three scripts pass Ruff.
- `work/analysis/radial_marker_v245/repair_plan.json`, `saved_proof.json`, `live_proof.json`.
- `six_baked_caption_comparison.png` and`six_caption_repair_preview.png` in that
  analysis directory; full before/after previews were visually reviewed.
- `work/emulation_v193/radial_marker_v245/capture_report.json` and frame PNGs.

Continue auditing older baked-label erase bounds for the same leftover-stroke
class. Four unreadable Online bodies, other embedded/environmental/alternate
consumers, name consistency and final whole-scope visual/gameplay verification
remain incomplete. Do not treat the stored-art fix or this scoped cold boot as
completion of the full goal. Revisit older record-based checks at eventual
completion as requested.
