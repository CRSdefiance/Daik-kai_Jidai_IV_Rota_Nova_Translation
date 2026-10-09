# Japanese graphics audit against saved V150

## V227: complete stored glyphs verified for all57 native/compact labels

All48 original-font and9 compact labels pass full source-ink, blank-cell and bound
checks against actual V218 pixels:24,864 pixels total. Every first/last letter,
symbol and punctuation mark is present. All57 tight previews were visually reviewed
at source scale; no old-label foreground or clipped glyph is found in their text
extents. This is stored-bitmap proof; native consumer crops/alpha/gameplay remain
separate. V218 unchanged; full goal active. See [V227 glyph review](native_label_glyph_review_v227.md).


## V226: registered graphics pixel ownership passes

All48 graphic entries changed after the canonical baseline have registered edit
ownership. Across81 registered entries, zero new pixel changes occur outside their
owned boxes/slots. The4,998 initially flagged pixels are existing accepted artwork
already in the canonical ROM and preserved exactly. Inside-box borders/letters,
native crops/alpha and gameplay remain separately scoped; full goal active.
V218 unchanged. See [V226 pixel ownership](graphics_pixel_ownership_v226.md).


## V225: whole 921-entry graphics preservation gate passes

All660 PXL and261 FLS entries preserve original format flags, dimensions/pitch,
palettes and complete payload extents in V218. There are84 changed graphic entries.
This is whole-inventory preservation evidence, not translation/border/crop/alpha
or gameplay completion. Exact original Online24/27/31/33 images and hashes are
exported for source recovery; higher-resolution originals/manual scans have been
requested because their remaining body/chat text cannot be faithfully transcribed.
Independent full-scope work remains open. See [V225 preservation](whole_graphics_preservation_v225.md).


## V224: embedded pixel copies and raw FLS reader support verified

Four complete chara PXL pixel payloads match DSCHR exactly (143,360 bytes), with
palette/parent relationships still separate. OCINIT ship anchors remain partial;
459 differences prevent synchronization. The shared FLS reader now handles raw
archive storage, decoding the harbor illustration and all261 FLS textures without
exceptions. All660 PXL payloads are accounted for, including42 direct-color assets.
Raw FLS serialization is byte-exact, and the full registered V218 rebuild matches
its original SHA-256 after the reader change. No ROM bytes change; full goal active.
See [V224 copies and reader](raw_pxl_copies_and_fls_reader_v224.md).


## V223: OCINIT native loading and shared palettes verified

Seven original texture-table entries pass complete native read/transfer and guard
checks, covering 176,128 of 194,560 source bytes. The actual normal initializer
uses six; the seventh is an explicit table case. All thirteen shared startup
palette transfers are source-pinned. The remaining 18,432-byte tail and texture/
palette/parent relationships stay open; noisy color diagnostics are not asset
clearance. V218 is unchanged; full goal active. See [V223 loading evidence](ocinit_loading_palettes_v223.md).


## V222: all 56 TITLEMAP deferred placements and bounds verified

Native map queue calls pass with complete source preservation, guards and ABI.
All placements are (52,36)-(204,156) with priority 401, inside a DS screen.
The real argument is an integer priority, and C9904 processes the UI hierarchy;
previous direct-blit/render assumptions are corrected. Queue placement does not
prove framebuffer pixels or gameplay selection, which remain open. V218 is
unchanged; the full goal is active. See [V222 bounds](titlemap_queue_bounds_v222.md).


## V221: all 56 TITLEMAP records and source-art decisions verified

The actual record size is 18,752 bytes: a 152x120 indexed image plus its 512-byte
palette. All 56 native reads, palette preparation, bitmap constructors, relative
pointers and guards pass, covering the full 1,050,112-byte file. Complete source
views show geographic clue maps, decorative borders/motifs and red markers without
readable Japanese instructions. Retain their original pixels and palettes. The
final copy call queues a drawable; its subsequent scene render/crop binding remains
unverified and is not claimed from the source views. V218 is unchanged; the full
goal remains active. See [V221 source classification](titlemap_source_classification_v221.md).


## V220: five small sea-effect source-art decisions recorded

All sixteen palette variants of GMONS 2/4 and OCETC 2/5/6 were inspected.
Their complete source forms show sail/boat-like, splash, rounded-water, foam and
rippling-effect imagery without readable Japanese captions. Preserve the original
bytes. Alpha-bearing and tile-layout diagnostics did not justify a replacement
format or artwork repair. Combined with V219, source-content decisions cover all
14 records; exact native parent dimensions, palette/UV/alpha selection remain open.
V218 is unchanged and the full goal remains active. See [V220 review](raw_small_effect_art_v220.md).


## V219: raw sea-art readers and nine retain decisions verified

All 14 GMONS/OCETC records execute native reads and upload dispatch, covering
178,176 source bytes with exact offsets, source data, handles, guards and ABI.
Seven native texture-format cases establish the fixed and variable four-bit
presentations. Nine complete creature/weather/water source entries and all sixteen
palette variants are reviewed and retained unchanged, with no readable Japanese
instruction or caption. Five small record layouts remain unresolved; no whole-file
text-free clearance is claimed. TITLEMAP/OCINIT/DSCHR reader leads are located.
V218 remains the current ROM; full graphics scope stays active. See [V219 classification](raw_sea_art_classification_v219.md).


## V218: no-attack-target notice localized and cold-boot verified

The separate notice now reads "There are no targets to attack." in two complete
natural rows. Both native source consumers select English. The larger sprite copy
is placed after the original uploads to preserve existing artwork; the ordinary
bitmap uses a verified continuation guard and enlarged view. The actual visible
notice passes 304 ink/4,096 foreground-and-blank pixels. All other 94,208 frame
pixels are identical to V217; four inherited help panels and full title, New Game,
story and town frames also pass. All 467 prior batches and other files/ARM7 remain
intact, and the clean-ROM patch reconstructs V218 exactly. The alternate ordinary
bitmap's physical use remains separate from the verified packed sprite display.
Full graphics scope remains open. See [V218 checkpoint](all_routes_unified_v218_checkpoint.md).


## V217: complete English sailing panels integrated and cold-boot verified

Info, Search and Declare War now display complete natural English. Four native
producer paths and four parent variants pass, including the duplicate first-opening
Info source. V216 is revoked because that initialization path remained Japanese.
V217 passes four actual mode captures: 180,224 exact foreground/blank pixels and
5,496 ink pixels, with complete first/last letters and no footer overlap. Title,
New Game, story and town were reviewed. All 467 inherited batches/files and ARM7
are preserved; the clean-ROM patch reconstructs the registered ROM exactly.
The separate no-target notice remains Japanese and is mapped/reviewed for the next
repair. Four Online bodies and the remaining naming/raw/native/context/gameplay
scope stay open; the full graphics goal remains active. See [V217 checkpoint](all_routes_unified_v217_checkpoint.md).


## V215: native sailing-panel packed screen mapping

Original producer output matches eight Search-panel regions in all 25,600
foreground/blank pixels. The 32x16 bank arrangement, heading offset (56,2),
and narrower first/third body source regions are established. Linear bitmap
copying remains incompatible. Other modes and protected English production,
live display and registered integration remain open. V211 unchanged; full goal
active. See [mapping and scope](sailing_panel_packing_v215.md).

## V214: sailing-panel producer and full English layouts

All three original overlay producer calls return with exact CP932 lookup sequences
and guards. Complete English previews use the actual ROM font, automatic wrapping
and every source instruction; two/five/five body rows fit the proposed canvas.
Native sprite packing/callback and English mode display still require proof, so
no ROM change or formatting-gate completion is claimed. V211 remains current and
the full goal active. See [calibration and layouts](sailing_panel_calibration_v214.md).

## V213: three additional Japanese sailing panels confirmed

A fresh normal sailing run shows Japanese Info/Search/Declare War instructions.
The actual source pointers and overlay renderer are mapped; complete natural
English is source/context reviewed in a manuscript. Native formatting and English
display are still pending, so no layer is registered or screen claimed fixed.
These are additional remaining graphics beyond the four Online files. V211 is
unchanged and the full goal remains active. See
[live evidence and translation](live_sailing_mode_panels_v213.md).

## V212 research: complete RACE reads and generated-mode paths

Seven original native record reads cover all 851,296 RACE bytes with exact source
and guards. Geographic diagnostics remain numerical interpretation research;
BGR555 coloring is not display clearance. Two original metadata/read-size
discrepancies remain unmodified. DSCHR mode paths reference Japanese exploration/
war instructions and the real overlay text parser; active display and translated
alternatives still need tracing. No ROM change; V211 current, full goal active.
See [evidence and scope](race_records_and_generated_modes_v212.md).

## V211: missed embedded START instruction localized and integrated

DSOBJR contained a Japanese copy of the title START/touch instruction. Its native
banked payload now reuses the accepted English title02 artwork, with all source
indices, transparent padding and unowned prefix/palette bytes verified. All 467
batches and prior stages are retained; V205 reproduces exactly, only DSOBJR
changes, and the clean patch reconstructs V211 exactly. Complete displayed prompt
letters/background (8,192 native pixels), New Game, established dialogue and town
UI pass two fresh cold boots. V211 is experimental; four Online bodies and the
remaining graphics scope stay open. See [checkpoint](all_routes_unified_v211_checkpoint.md).

## V210: native common atlases and real market display

862 actual portrait/item reads and trade/compact crop constructors pass exact
source bytes, palettes, bounds and guards. All 684 item/trade source cells were
reviewed on ten sheets and retained as object paintings. Normal V205 market
navigation reaches Deal; five complete quantity masks and source artwork match
2,855 pixels. Another 25 white GUI-indicator pixels remain independently unmapped,
so full composition is not claimed. Legacy common-block relationships and the
eleven-block census remain open. No ROM change; full goal active. See
[evidence and scope](common_atlas_consumers_v210.md).

## V209: native SLACK helper selects loose sprites, not raw comics

All21 valid slots execute the original owner/header/view/virtual-copy/cache path
with exact full PXL bytes and guards. Slots13-19 alias the 44x60 English name-label
sprite; they do not display raw same-numbered archive blocks through this helper.
All14 unique source images were reviewed and existing English artwork preserved.
Main sections and the one ARM9 overlay contain only the three mapped direct helper
callers; computed/indirect alternatives remain unruled out. This is scoped native
consumer evidence, not raw-comic GPU clearance. V205 is unchanged, the eleven
unresolved ILNK blocks remain open and the full goal stays active. See
[consumer mapping and limits](slack_viewer_consumers_v209.md).

## V208: sky source layout resolved and all fourteen views retained

Native texture commands prove the regular linear 256x32, 256-color layout. All
122,880 source indices and fourteen palettes are preserved in complete reviewed
views; no composed text is observed, so retain the source environmental artwork.
Normal V205 sailing was cold-booted and reviewed. Exceptional extra sampling and
projected sky/crop checks remain open; no ROM changed and full goal stays active.
See [source decision and evidence](sky_texture_geometry_v208.md).

## V207: complete sky-file partition and character-font retain decision

All 14 native SKYWALL reads cover its complete 130,048 bytes with exact source
payloads, trailing palettes and guards. Diagnostic views were reviewed, but
assembled BG geometry and scene/GPU checks remain open. The current 3,340-cell
KANJI.FNT is verified as the original source character font and retained; it is
not composed artwork requiring glyph-by-glyph translation. The eleven unresolved
ILNK blocks remain unchanged. No ROM change. See
[raw-resource evidence](raw_sky_and_font_classification_v207.md).

## V207: retained Tavern/Inn sprites and English labels displayed

Both unchanged sprites match all 2,171 opaque source pixels in a fresh native
display fixture. D-pad navigation selects complete Tavern/Inn captions: all nine
glyph cells and 107 ink pixels pass, including first/last letters and bounds.
Only the alternate image/hit selectors are forced; normal city assignment and
alternate-city caption anchors remain unproved. Four town backgrounds remain
open. V205 is unchanged; full goal active. See [display evidence](contextual_environment_display_v207.md).

## V206: retained environmental signs mapped to native facility consumers

The source wine lantern is the Tavern icon and the tiny plaque is the Inn icon,
with separate English captions verified by real clean/current getters. Both native
icon selector branches/cache loads and all four dynamic town-background reads
preserve complete source headers/palettes/pixels with guards and ABI intact.
This supports the six retain decisions; it does not invent plaque/shop readings or
prove all city/GPU/crop/gameplay use. No artwork or ROM changed; V205 remains
current and full goal active. See [V206 evidence](contextual_environment_native_v206.md).

## V205: source-backed Online31 speaker name

Julien replaces the clear ジュリアン label using official bilingual name evidence.
The palette, dimensions, headers, borders, portraits and every outside-box index
remain exact; only the owned name-box background uses a donor estimate. Complete
native screenshot/glyph checks and registered ROM/patch inheritance pass. The
unreadable dialogue/chat and all four screenshot bodies remain open. Newly fetched
official guide movies contain 81 reviewed static bitmaps but no exact source frame.
Goal active; V205 experimental. See [proof and scope](all_routes_unified_v205_checkpoint.md).

## V204: Hodram source-native opening name art complete

Twenty revised native textures reconcile Hoodlum with the confirmed Hodram name;
the existing H/Ho prefixes and all other artwork remain exact. All 22 reveal states
match native pixels, including black shadows, complete first/last letters and
display bounds. All palettes, dimensions and flags are preserved, and pixel slots
reclaim only guarded zero alignment padding. The registered combined ROM/patch,
full V190 reproduction and cold-boot regression checks pass. This finishes that
specific opening-artwork consistency item; four Online bodies and remaining
classification/context/native/gameplay/name-migration work remain. Goal active;
V204 experimental. See [checkpoint](all_routes_unified_v204_checkpoint.md).

## V203: fourth captain portrait verified through an explicit selection fixture

Maria's full 104×136 portrait matches all 14,144 native pixels. All four captain
portraits now have complete static pixel evidence (56,576 total); the fourth uses
a documented test-only selection limit, not a legitimate unlock. Her four name/
company fields match 246 native font pixels including first/last letters and blank
cells. Runtime FI/FA/FO/FU outputs are measured from her actual initialized player
object without getter bridges. No registered ROM or artwork changed; broader goal
gates remain open. See [V203 evidence and limits](maria_native_widgets_v203.md).

## V202: four actual captain portrait owners; three complete live crops

Actual native parent field copies and cache loads prove the four 104×136 loose PXL
owners and their complete palettes/index data. Native read tracing observes no
legacy-buffer reads in that tested path. Three complete cold-boot portraits match
42,432 five-bit pixels, including every edge/background pixel. All four complete
source portraits were reviewed and retained as paintings without written UI text.
The fourth live display and the legacy buffers' own palette/other-consumer meaning
remain open; the eleven-block storage census is unchanged. V190 and all artwork
remain unchanged; goal active. See [V202 proof and limits](native_captain_portrait_binding_v202.md).

## V201: confirmed-name consistency research advances

The full-name catalog preserves script/resource bytes and supplies the complete
chosen names in all 25 remaining short slots. Canonical/clean locks, complete
four-route matching scope, startup and native-copy proofs pass. All 25 previews
were reviewed; four source/context wording problems were corrected. A real
cold-boot smoke matches 817 complete native text pixels, including first/last glyphs.
This is research toward text/artwork naming consistency, not new localized graphics
or broad graphics clearance. The movie's Hoodlum-to-Hodram replacement, four Online
bodies and all remaining classification/native/gameplay gates stay open. V190 remains
the latest registered ROM. See [V201 evidence](confirmed_name_catalog_v201.md).

## V197 original Latin name cards: complete native lettering

Fresh V190 cold-boot frames match all 7,132 nonblack source glyph/outline pixels
for Rafael Castor, Hoodlum Joakim Bergstrom, Camille Overijssel and Lil Argot.
Selected complete lettering bounds include first and last letters within the top
display. A later ten-pixel dim-edge animation difference is recorded separately;
every temporal crop/alpha effect is not yet classified. The original artwork is
retained. Name migration remains open due to 42 text formatting/allocation failures.
See [source/native evidence](latin_name_migration_and_native_cards_v197.md).

## V186 smoother Rota Nova title copies

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

## V185 reaction and reveal effects; requested pause

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

## V184 decorative Maria titles and visiting dialogue

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

## V183 complete creature introduction; native display open

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

## V182 complete chase dialogue; native display open

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

## V181 bounded comic captions and credits

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

## V180 Maria heading and player thanks

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

## V179 complete closing gallery lettering

2026-10-04. Raw block19 frame16 is English; frames18/19 retain painted
attribution marks with explicit source-based decisions. Nine embedded caption/
credit images and four historical Online files remain. **47 tests**, full V178
reproduction, complete 463-batch inheritance and exact patch reconstruction
pass. Full glyph reconstruction rejects rehashed first/final-letter loss;
connected gray portrait edges are protected. Native loader/geometry/alpha/GPU/
gameplay and broader graphics gates remain open; unclassified counts unchanged.
See [V179 checkpoint](all_routes_unified_v179_checkpoint.md).

## V178 clipped-source preservation

2026-10-04. Image207's unidentified top-edge stroke is retained exactly while
its complete English caption/placement remain unchanged. **43 focused tests**,
controlled glyph/header and exact ROM/patch checks pass. Only image207 differs
from V177; **462 experimental batches**. Four Online files and 12 embedded
comic/credit images remain, plus broader source/native/gameplay gates. Source
interpretation and actual native use remain open.
See [V178 checkpoint](all_routes_unified_v178_checkpoint.md).

## V177 source-backed bubbles and contextual-art review

2026-10-04. Four Online27 bubble phrases are English; reduced chat/status remain.
Only that file differs from V176; **462 experimental batches**, **65 focused
tests**, controlled header/crops and exact patch reconstruction pass. Four
historical Japanese-bearing files still remain. Six source-resolution
environmental paintings/lanterns retain their original physical decoration;
decisions are recorded in `translations/contextual_graphics_decisions_v177.json`
and byte-exact in V177. Native usage/captions remain open. All 42 raw block-13
portraits were inspected; no Japanese caption observed, native partition still
unproved. Broader full-resolution/source/native/gameplay gates remain open.
See [V177 checkpoint](all_routes_unified_v177_checkpoint.md). Goal active/incomplete.

Subsequent source-word review revealed **12 text-bearing comic/credit images**
in SLACKIMG block 19, outside the historical PXL/FLS inventory. All 21 coherent
sketch previews were inspected. Japanese/Chinese captions, dialogue/effects and
creator signatures need translation or retention decisions; native partition/usage
remain unproved. These are additional to the four historical Online files.

## V176 title localization continuation

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

`inventory_graphics_v150.py` inventories the exact combined V150 ROM and exact
clean comparison ROM. It renders all **660 PXL files** and all **261 textures
in 15 FLS files**: **921 previews**, zero decode errors, 116 contact sheets.
Palette PXL files roundtrip byte-for-byte. All 42 direct-color PXL files have
checked word/pixel extents and opaque BGR555 previews; native alpha is unproved.
The exceptional `/m02_03.fls` has one raw 512-byte palette and 262144-byte pixel
block, unlike the other compressed FLS records. Its verified raw storage preview
is 512 square; visible composition and its 377-height field remain unproved.

The complete inventory is `work/analysis/graphics_v150/inventory.json`.
Rendering does not classify text. Dynamic text, other graphics containers,
native palette/alpha/composition and physical gameplay require separate review.

## First visual review

Six UI contact sheets screen 43 assets. The durable source/hash-bound review is
`translations/graphics_visual_audit_v150.json`. Four assets visibly retain
Japanese:

| Resource | Remaining work |
| --- | --- |
| `/_pxl/__frame.pxl` | Calendar/month/year and multiple baked menu/button labels; source transcriptions and native crop mapping required. |
| `/_pxl/__marker.pxl` | Main captions are English, but small kanji symbols remain, including male/female; map their meaning and cropped icon usage. |
| `/_pxl/logo.pxl` | Main Japanese title and small subtitle remain in the artwork; review English title art and native uses. |
| `/_pxl/mysterymap/mys_hunt_d.pxl` | Header **秘宝名**; natural English draft **Treasure Name**. |

The frame and marker atlases were also inspected at full source resolution;
the treasure header was inspected in a 4x crop. The treasure resource's clean
ARM9 table entry at `021107C4` contains path pointer `0216151C` and runtime image
owner `02313A10`. This is a data record, not executable consumer proof. Draw
geometry, palette and loader/crop mapping are still required for integration.

The other 39 UI thumbnails show no obvious Japanese at their contact-sheet
scale. This does not clear small lettering, tall atlases or unseen composition.
The initial pass left 878 previews unreviewed; the continuation below supersedes
that count. No ROM, registry, formatting
approval or candidate changed. V150 remains experimental and unchanged.

## Continued screening: 299 assets

Contact sheets `remaining_000`–`remaining_027` and `remaining_068`–`remaining_071`
add 256 inspected previews. Combined with the first 43 UI assets, the durable
audit now has **299 screened assets**, **nine confirmed Japanese resources**,
and **622 previews not yet reviewed**. The added sheet hashes and exact asset
IDs are saved in the audit. Screening is not exhaustive clearance of reduced
images, tall atlases, small symbols or native composition.

Five additional resources visibly contain Japanese:

| Resource | Source and next work |
| --- | --- |
| `/_pxl/deck04.pxl` | Digits followed by **勝 / 敗** (wins/losses). Determine the actual score consumer and sprite-cell width before English labels. |
| `/_pxl/slackimg12.pxl` | **名 / ミドルネーム / 姓 / 勢力名 / 誕生日**: name, middle name, surname, faction/company name and date of birth. Map this alternate plaque set's usage and crops. |
| `/_pxl/slackimg20.pxl` | **ボタンを押してください！**; natural draft **Press a button!** Verify its input context and crop. |
| `/_pxl/startmenu0.pxl` | Japanese main title and subtitle in Porto Estado title art. Native use and English artwork pending. |
| `/_pxl/winframe00.pxl` | Japanese main title and subtitle in Porto Estado window/title art. Native use and English artwork pending. |

The deck atlas and both small label/prompt atlases were individually inspected
at 4x source resolution. These three files are byte-identical to clean Japanese.
The viewed opening FLS subtitle textures contain English; this does not approve
all opening dialogue's naturalness or source fidelity.

`kbj04.pxl` and `kbj08.pxl` also contain East Asian environmental sign artwork.
The lantern character resembles 酒. Language, context and intended localization
are unresolved; these signs are recorded separately from confirmed Japanese UI.
Do not erase contextual artwork merely because it contains an East Asian glyph.

## Continued screening: 491 assets

Contact sheets `remaining_028` through `remaining_051` add 192 inspected
previews. The durable audit now records **491 screened assets**, **15 confirmed
Japanese resources** and **430 unreviewed previews**. Inventory identity, exact
asset hashes, sheet hashes and unique resource/texture pairs were checked when
saving these observations. This supersedes the earlier screening counts.

The six newly confirmed resources are:

- `/_pxl/online/Online24.pxl`: Japanese item/inventory UI and chat in a baked PC screenshot.
- `/_pxl/online/Online27.pxl`: Japanese town chat bubbles and UI chat in a baked PC screenshot.
- `/_pxl/online/Online31.pxl`: Japanese portrait/dialogue text and chat in a baked PC screenshot.
- `/_pxl/online/Online33.pxl`: Japanese quest/inventory UI and chat in a baked PC screenshot.
- `/_pxl/title/title03.pxl`: Japanese DS main logo and small Rota Nova subtitle.
- `/_pxl/title/title05.pxl`: Japanese DS main logo and small Rota Nova subtitle over water.

The promotional English text cards are readable at this preview scale, but this
does not approve their full source fidelity or native rendering. Scene artwork
in these pages has no obvious Japanese UI lettering. Small lettering and
decorative environmental signs still require closer inspection and language/
context classification; these thumbnails do not establish exhaustive clearance.
No ROM, release registry or integration approval changed. V150 remains unchanged.

## Continued screening: 619 assets

Contact sheets `remaining_052` through `remaining_067` add 128 inspected
previews. The audit now records **619 screened assets**, **23 confirmed Japanese
resources**, and **302 unreviewed previews**, superseding earlier counts. Exact
inventory identity, resource hashes, sheet hashes and record uniqueness were
checked before saving.

Eight white scene images contain handwritten Japanese labels:
`/evstill/evstill168.pxl` through `evstill171.pxl`, and
`/evstill/evstill206.pxl` through `evstill209.pxl`. The first group labels Arab,
New World, Chinese and North Sea villages; the later group labels corresponding
development scenes. These appear to be placeholder artwork, but appearance does
not prove they are unused. Full source transcription, native usage, and the
appropriate English replacement or evidence-backed exclusion remain pending.

The other scene and initial logo/FLS texture previews show no obvious Japanese
UI lettering at this scale. Small environmental lettering and native composition
remain unclassified. No ROM, registry or integration approval changed.

## Continued screening: 731 assets

Contact sheets `remaining_072` through `remaining_085` add 112 inspected
previews. The audit now records **731 screened assets**, **25 Japanese-bearing
assets**, and **190 unreviewed previews**. These counts include separate texture
records within a single FLS file; they are not counts of distinct ROM files.
Exact inventory identity, resource hashes, sheet hashes and record uniqueness
were checked before saving.

`/FLS/M28.fls` textures 4 and 5 contain the Japanese main title and small
Japanese Rota Nova subtitle. Both are byte-identical to clean. Native composition
and English artwork remain pending.

The same file has clean-original progressive Latin name cards: Rafael Castor,
Hoodlum Joakim Bergstrom, Lil Argot and Camille Overijssel. Review consistency
against established dialogue names before deciding replacements; original Latin
art is evidence, not automatic approval of project naming. Textures 33, 34 and
36 were inspected individually at full resolution: each retains the initial H.
Reduced contact-sheet appearances do not establish missing leading characters.
Later frames show longer text; native animation/crop behavior still needs review.
No ROM, release registry or integration approval changed.

## First PXL/FLS screening complete: 921 assets

Contact sheets `remaining_086` through `remaining_109` add the final 190
previews. All **921 inventory records** are now screened exactly once; **26
Japanese-bearing assets** are confirmed. Source identity, sheet/resource hashes
and complete equality of audited resource/texture keys with the inventory pass.
This completes thumbnail screening only. Full-resolution, native composition,
source fidelity and translation/integration approval remain open.

`/Iseki/dock.pxl` contains baked Japanese fleet-row labels for the flagship and
ships 2 through 5. It is byte-identical to clean. Transcribe the source and map
native consumers/crops before English artwork is integrated.

`/towngrp/towngrp32.pxl`, `towngrp33.pxl`, `towngrp35.pxl` and `towngrp37.pxl`
have small East Asian environmental sign/plaque marks. These are recorded for
language/context review, not assumed Japanese UI or excluded automatically.
The full-resolution town37 image still does not support reliable transcription.
The reviewed ending textures have no obvious Japanese UI at preview scale;
native composition and small contextual lettering are not cleared.

No ROM or release registry changed. Next steps are close inspection and actual
localization of confirmed assets, plus inventory of graphics formats outside
PXL/FLS. The zero unreviewed-thumbnail count does not complete the graphics goal.

## Graphics resources outside PXL/FLS

`scripts/inventory_other_graphics_v150.py` pins the exact V150 and clean ROMs
and inventories all 714 filesystem files. Their extensions are 660 PXL, 15 FLS,
35 DK4, and one each of FNT, SDAT, 000 and BIN. Thus 39 files lie outside the
PXL/FLS inventory. Complete path equality with clean and unique paths are checked;
extension and directory names do not classify content or establish native use.
Metadata is saved in `work/analysis/other_graphics_v150_inventory.json`.

Seventeen resources are under `/GRP`. Six strict ILNK archives contain 57 blocks:

| Archive | Blocks |
| --- | ---: |
| BUSTUP.DK4 | 2 |
| CHARA.DK4 | 14 |
| CMMNIMG.DK4 | 10 |
| MAPPOINT.DK4 | 4 |
| SLACKIMG.DK4 | 21 |
| WINFRAME.DK4 | 6 |

All six archives parse/rebuild byte-exactly. None of their complete block hashes
matches a complete loose PXL file in either clean or V150. This does not exclude
shared image payloads, alternate headers, compression or dimensions; block
decoding and native mapping remain necessary. The other GRP resources include
DSCHR, DSOBJ, DSOBJR, GMONS, OCETC, OCINIT, RACE, SKYWALL, TITLEMAP, CMMNIMG.000
and the known KANJI font. Previously accepted DSOBJ radial labels must be preserved.
No resource is cleared solely because its hash is unchanged from Japanese.
No ROM or release registry changed during this inventory.

## Next work

Finish close visual review of PXL and FLS previews, audit the other graphics
containers, and translate confirmed labels from clean source with natural English.
Preserve source dimensions, palette roles and unrelated art; verify complete
rendered letters and actual native crop/composition before combined integration.
