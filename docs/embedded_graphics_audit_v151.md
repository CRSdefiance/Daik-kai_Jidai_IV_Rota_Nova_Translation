# Embedded graphics: V151 storage audit

## V211: missed embedded START instruction localized and integrated

DSOBJR contained a Japanese copy of the title START/touch instruction. Its native
banked payload now reuses the accepted English title02 artwork, with all source
indices, transparent padding and unowned prefix/palette bytes verified. All 467
batches and prior stages are retained; V205 reproduces exactly, only DSOBJR
changes, and the clean patch reconstructs V211 exactly. Complete displayed prompt
letters/background (8,192 native pixels), New Game, established dialogue and town
UI pass two fresh cold boots. V211 is experimental; four Online bodies and the
remaining graphics scope stay open. See [checkpoint](all_routes_unified_v211_checkpoint.md).

## V186 opening-title styling; broader native gates remain

2026-10-05. Focused user-requested correction: **Uncharted Waters IV**
now has smooth blue beveled lettering with shaded edges, replacing the prior
binary-alpha, thick white outline. The small **ロッタ ノヴァ** label is a phonetic
rendering of Rota Nova; its redundant English duplicate is omitted from all four
Rota Nova title copies. Original gold-logo pixels, copyright, palettes, native
headers/records/dimensions and unowned scenery remain preserved.

**15 focused tests**, whole byte-identical V185 reproduction, all **463 registered
batches** and inherited terminal stages, exact saved artwork/manifest identity,
and clean-ROM patch reconstruction pass. Only M28 and the three Rota Nova PXL
title resources change versus V185. V186 is experimental; native display and
cold-boot acceptance remain pending. The broader graphics goal **stays paused**.
See [V186 title checkpoint](all_routes_unified_v186_checkpoint.md).

## V185 frames6/7; interpretation and native usage open

2026-10-04. The requested next two comic panels (raw block19 frames6/7)
have complete **Huh?!** and decorated **TA-DA!** English lettering. The universal
question mark and ambiguous brown water shapes are preserved without assigning
the latter a reading or anatomical meaning. Their interpretation remains open.
Source creature cores, people, lower waves, photo border, earlier artwork and
unowned pixels are exact. Covered paper/sea estimates remain **approximate**.

**113 focused tests**, final full byte-identical V184 reproduction, all **463
registered batches** and inherited terminal stages, saved ROM identity/content,
and exact clean-ROM patch reconstruction pass. Only `/GRP/SLACKIMG.DK4` changes
versus V184; ARM9 is unchanged. V185 is **experimental**, with no cold-boot
acceptance assumed. See [V185 checkpoint](all_routes_unified_v185_checkpoint.md).

The graphics goal is **paused at the user's request** after this image batch
and combined ROM compilation. It is incomplete. Four Online files, interpretation
of the retained frame6 marks, unclassified/contextual art and broad source/native/
display/gameplay gates remain. Resume only when requested. Keep the requested
older record-based-check follow-up for eventual full completion.

## V184 frames11/12 lettering; raw native usage open

2026-10-04. Raw block19 frames11/12 have complete **Maria Mode** headings
across their original colored name tiles/letters and horizontal/vertical titles.
Frame11's red Chinese visiting bubble is natural English, automatically wrapped
at 9px inside the original elliptical border. No unsupported Ta-da phrase is
added. Original visible tile edges, bubble contour, prior artwork and unowned
pixels remain exact. English Mode receives an English lettering shadow; covered
flat tile backing estimates remain **approximate**.

**129 focused tests**, final whole byte-identical V183 reproduction, complete
**463-batch** inheritance and exact saved ROM/patch reconstruction pass.
Only SLACKIMG changes versus V183. **Two embedded images** (6/7) and
**four Online files** remain, plus broad source/native/graphics/gameplay gates.
Actual raw loading/display remains unproved; unclassified counts unchanged.
No cold-boot acceptance assumed. See [V184 checkpoint](all_routes_unified_v184_checkpoint.md).
Goal active/incomplete.

## V183 frame8 bubble lettering; original portraits exact

2026-10-04. Raw block19 frame8 now has complete **...Who are you?** and
**Sea cow.** lettering at 11px. Sea cow is a documented comic localization of
the source sea-slug/cow wordplay following the bullfighter declaration; it is
an editorial inference, not an official creature-name or biological claim.
Original portraits, whole traced bubble contours/tails, unowned pixels and
all earlier artwork remain exact. No new scenery restoration is introduced.

**111 focused tests**, full byte-identical V182 reproduction, complete
**463-batch** inheritance and exact saved ROM/patch reconstruction pass.
Only SLACKIMG changes versus V182. **Four embedded images** (6/7/11/12)
and **four Online files** remain, plus broader source/native/graphics/gameplay
gates. Actual raw loading/display remains unproved; unclassified counts unchanged.
No cold-boot acceptance assumed. See [V183 checkpoint](all_routes_unified_v183_checkpoint.md).
Goal active/incomplete.

## V182 frame5 chase dialogue; native raw usage open

2026-10-04. Raw block19 frame5 has all four chase phrases in natural English:
**I'm gonna be a great bullfighter!**, **I said, let's go to sea!**, **No way!**
and **Hey! Get back here!**. Both bubble phrases use complete 9px lettering;
the refusal uses the source maroon color. Original visible outlines, protected
bubble corners, earlier artwork and all unowned pixels remain exact. Scenery
and outline pixels concealed by source lettering are **approximate**.

**99 focused tests**, final whole byte-identical V181 reproduction, full
**463-batch** inheritance and exact saved ROM/patch reconstruction pass.
Only SLACKIMG changes versus V181. **Five embedded images** (6/7/8/11/12)
and **four Online files** remain, plus source/native/graphics/gameplay gates.
Actual raw loaders/display remain unproved; unclassified counts unchanged.
No cold-boot acceptance assumed. See [V182 checkpoint](all_routes_unified_v182_checkpoint.md).
Goal active/incomplete.

## V181 recruitment/end captions; native raw usage open

2026-10-04. Raw block19 frames4/10 have complete **Recruiting New Crew**,
source-kana creator credits, and **The End.** English lettering. Credits directly
romanize the parenthetical Madogiwa Deka without inferring a title/alias. Full
English stays outside the photos; only old glyph/fringe masks are restored.
Same-photo canonical donors preserve detail, with bounded local fallback;
hidden scenery is **approximate**, not claimed recovered original. Original
unowned art/borders, prior raw frames and atlas syncs remain exact.

**78 focused tests**, full byte-identical V180 reproduction, complete **463-batch**
inheritance and exact saved ROM/patch reconstruction pass. Only SLACKIMG changes
versus V180. **Six embedded images** (5/6/7/8/11/12) and **four Online files**
remain, with source/native/graphics/gameplay gates open. Native raw loaders/display
are unproved; unclassified counts unchanged; no cold-boot acceptance assumed.
See [V181 checkpoint](all_routes_unified_v181_checkpoint.md). Goal active/incomplete.

## V180 Maria artwork; raw native usage remains open

2026-10-04. Block19 frame13 now has complete **Maria Mode** and **Thanks for
playing all the way through...** lettering. Both painted creator credits remain
byte exact with explicit retain decisions. Review caught and removed leftover
source ellipsis dots. **59 focused tests**, full byte-exact V179 reproduction,
all **463 batches/stages** inherited and exact ROM/patch reconstruction pass.
Only `/GRP/SLACKIMG.DK4` differs from V179, within two frame13 text regions;
frame16 and both prior atlas syncs are exact. **Eight embedded caption/credit
images** (4/5/6/7/8/10/11/12) and **four Online files** remain, plus broader
source/native/gameplay gates. Native raw loader/display remain unproved;
unclassified counts unchanged. Goal active/incomplete; no cold-boot acceptance
assumed. See [V180 checkpoint](all_routes_unified_v180_checkpoint.md).

Latest: [V179 checkpoint](all_routes_unified_v179_checkpoint.md). Block19's
frame16 has complete English appreciation/title; every other frame and both
prior atlas syncs remain exact. Painted corner marks in frames18/19 retain
original attribution styling; no author name is invented. Nine caption/credit
images remain. New strict raw-art ownership, exact-font glyph reconstruction
and connected-edge protection pass 47 tests; full V178 reproduces exactly.
Storage partition remains a reviewed interpretation. Actual native loader/
geometry/alpha/crops/GPU/gameplay are unproved; unclassified counts unchanged.

Latest integrated checkpoint: [V178](all_routes_unified_v178_checkpoint.md).
Image207's original clipped mark is preserved; all embedded bytes are unchanged
from V177. Block-19 phrase drafts are saved in
`translations/embedded_sketch19_source_manuscript_v1.json`, with final layout/
visual gates open and no candidate applying them. Its 12 text-bearing images
remain additional translation/credit work; raw native formats remain unproved.

## V177 raw portrait visual review

SLACKIMG block 19 was also inspected as 21 full-size coherent 320×240 BGR555
sketch/comic previews. **12 images bear East Asian text**: Japanese
captions/dialogue/effects, Chinese dialogue and creator signatures. Indices
4/5/6/7/8/10/11/12/13/16/18/19 need translation or explicit credit decisions.
Source SHA `c95b9d4b968638d488158c8971c03f4116ac6e6ceb8a6863a4de5a1b05b54464`
is unchanged in V177. `scripts/inspect_raw_sketches_v177.py` and
`work/qa/embedded_raw_v177/sketch19/inventory.json` pin source-word roundtrip,
all preview hashes and reviewed sheets. This adds translation work outside the
PXL/FLS list. Native format/partition/usage remain open and unclassified counts
are not reduced.

2026-10-04. All words in SLACKIMG block 13 yield **42 coherent 320×240 BGR555
portrait previews** under the proposed partition. All 42 full-size previews were
inspected; no Japanese caption observed. Existing Latin El Gato apparel wording
is retained. Block bytes remain exact in V177. Source-word roundtrip, independent
preview hashes and seven reviewed sheets are pinned in
`work/qa/embedded_raw_v176/portrait13/inventory.json` by
`scripts/audit_portrait13_v177.py`. No native loader/metadata proves this format
or partition; **unclassified-block counts remain unchanged**. Other raw preview
hypotheses are not cleared. See [V177 checkpoint](all_routes_unified_v177_checkpoint.md).

## V176 native-sized WINFRAME storage localization

2026-10-04. Two loose Porto Estado titles and the original-sized **320×240**
embedded WINFRAME title now have complete Uncharted Waters IV / Porto Estado
English lettering. Original gold logo/bevels, copyright, palettes, headers,
allocation and all unowned pixels remain exact. Water restoration uses the
original donor; masked medallion reconstruction is approximate. All prior
translations/code/stages remain exact. Full V175 reproduction, **240 graphics
tests**, two controlled PXL headers, six supplied crop descriptors and exact
clean-ROM patch reconstruction pass. V176 is experimental, **461 batches**;
only the three title resources differ from V175.

Four historical Japanese-bearing Online screenshots remain, plus broader
embedded/unclassified/contextual art, source fidelity, full-resolution and actual
native/gameplay checks. V175 feedback remains pending; no cold-boot acceptance is
assumed. The graphics goal remains active.
See [V176 checkpoint](all_routes_unified_v176_checkpoint.md).

## External-palette continuation reviewed on 2026-10-02

Three further storage pairs have now been visually inspected. CMMNIMG blocks
4/5 contain a Japanese menu/button/marker atlas. Its right half matches loose
`__frame.pxl` indices; palette equivalence and native use are unproved. Keep this
embedded copy in the translation backlog. MAPPOINT pairs 0/1 and 2/3 contain
decorative building/landmark glyphs; language/context remains unresolved.
All three archives are byte-identical in current V154 to the inventory source.
Six formerly unclassified blocks have bounded external palette/pixel storage,
leaving 21 unclassified. Native pairing, bank selection and composition remain
open. `translations/external_palette_graphics_visual_audit_v151.json` pins the
inventory, sheet, archive/preview hashes and these observations. No graphic
translation or formatting approval is claimed.

The exact saved V151 ROM is the source, SHA-256
`d61241e3f9d29debcc41cedcf7824aa06ac36e5e07643c714e7b045465c40345`.
No ROM changes were made. `inventory_embedded_graphics_v151.py` inspects all
57 blocks in six `/GRP/` ILNK archives and verifies exact archive reconstruction.
Thirty blocks contain bounded type-16 palette images. CMMNIMG block 1 contains
two consecutive images, giving **31 storage previews** inspected on four sheets.
Twenty-seven blocks remain unclassified; the other GRP resources also remain open.

## Storage boundaries

For the observed type-16 records, mode 8 has packed 4-bit indices and mode 9 has
8-bit indices. The palette starts at byte 20. The third header word minus 12
is its byte extent; dimension metadata follows the palette. A 12-byte metadata
record declares pixel-byte extent plus 12, an unclassified flags word, and
16-bit width-in-words and height. Packed pixels follow it. Every decoded image
has exact declared dimensions, bounded extents and byte-exact pixel repacking.
These observed storage contracts do not establish native loader semantics.

CMMNIMG block 1's first image ends at byte 14688. Its remaining 14688 bytes
contain a second independently bounded image, not padding. Both are portraits.
Five previews have multiple palette banks; bank zero is only a provisional
storage view. CHARA block 0 looks scrambled and needs native composition mapping.
Palette-bank selection, alpha, flags and runtime consumers remain unproved.

## Japanese text confirmed

| Archive block | Work remaining |
| --- | --- |
| `/GRP/SLACKIMG.DK4` 12 | Name-entry plaques. Pixel indices match `/_pxl/slackimg12.pxl` exactly, but palettes differ. Translate and verify both consumers. |
| `/GRP/SLACKIMG.DK4` 20 | Japanese button prompt. Pixel indices match `/_pxl/slackimg20.pxl`, but palettes differ. Existing draft: **Press a button!** |
| `/GRP/WINFRAME.DK4` 0 | Japanese PC title and subtitle. Storage dimensions differ from loose title art; native usage and title treatment remain open. |

Nineteen previews match loose PXL dimensions, bit depth and every pixel index;
sixteen also match the entire palette. This establishes content duplication,
not a shared runtime consumer. Embedded Japanese copies must remain in the
backlog even after a loose PXL is translated. The remaining 23 single-bank
thumbnails show no obvious Japanese; that is not full-resolution or native
composition clearance. Game Over, PORTO ESTADO, the Koei logo and HOIST THE SAILS!
are already visibly Latin in the inspected previews.

## Evidence and limits

`work/analysis/embedded_graphics_v151/inventory.json` records each block hash,
palette/pixel boundaries, preview hash, duplicates and unclassified blocks.
`translations/embedded_graphics_visual_audit_v151.json` pins that inventory and
records all 31 actual thumbnail reviews. Native formatting approval is false
throughout. Three confirmed embedded Japanese images are additional storage
assets; do not add them to the earlier 26 PXL/FLS count as unique text content.
V151 boot acceptance is still pending and the full translation goal remains open.

## V172 continuation: shared marker copy synchronized

2026-10-04. V172 reuses the complete accepted English marker atlas in its exact
embedded CMMNIMG left-half copy, bringing 24 major captions into that duplicate.
Only 4312 indices differ; all V171 frame pixels, other resources/code, palette
banks/headers/ornaments and inherited repair stages remain exact. Disjoint regions
of one block now merge with overlap/geometry/identity guards. Complete V171 ROM
reproduction, 150 existing + 16 new graphics tests, Ruff and exact patch pass.
453 batches: all 452 V171 batches unchanged plus one source-locked marker sync.
Only CMMNIMG differs from V171. Male/female kanji remain; twelve historical loose
resources and other embedded art remain. Native loading/consumers/crops/banks/GPU/
input/gameplay are pending. V172 is experimental; the full goal is incomplete.
See [V172 checkpoint](all_routes_unified_v172_checkpoint.md).
