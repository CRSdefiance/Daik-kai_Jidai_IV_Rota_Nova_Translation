# V205: Online Julien label and expanded primary-source research

## Registered candidate

- ROM: `out/all_routes_combined_v205_candidate.nds`, SHA-256
  `88444cb34139aada935f81b39b478fa81b5f54a32ef7c88a7e08b2b3dfe1dfa0`.
- Profile: `all-routes-unified-v205`, experimental.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Preserves all 114 baked accepted layers, all 465 V204 batches/terminal stages and
  prior record IDs; adds `online31_julien_name_art_v1.json`, for 466 active batches.
- Only `/_pxl/online/Online31.pxl` changes from V204. ARM9, ARM7, all scripts,
  the Hodram opening correction and every other file/component remain exact.
- Patch: `out/all_routes_combined_v205_candidate.xdelta`, SHA-256
  `731ff6285b9f5bf97a9450f986d5c77dd09693cf3581160b6970ffe2c5110747`.
  Reconstruction from pinned clean ROM SHA-256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`
  produces the exact candidate. The manifest records full canonical-base changes.

## Source-backed name localization

The clear screenshot speaker name ジュリアン becomes **Julien**, following the
official English Online localization. The Japanese publisher's France episode and
the English operator's corresponding episode independently name this character.
The live saved HTML contains both forms, even though their presentation is omitted
by some text-only page readers. Source URLs and hashes are preserved in
`work/research/online_official_v205/Julien_primary_sources.json`.

Sources: [Japanese publisher](https://www.gamecity.ne.jp/dol/topics_cms/update/9787.html),
[official English operator](https://uwo.papayaplay.com/uwo.do?tp=lost_memories).
These later episodes establish the NPC spelling, not the historical screenshot's
unreadable sentence or location. This Online NPC is distinct from DK4's Julian
crew character; no global Julian rename occurs.

The 25×7 owned name rectangle is `[36,105,61,112]`. Complete seven-row bitmap
letters fit without resampling or cropping. Four existing compact glyphs are reused;
J/u are supplied as complete glyph definitions in the preparation script. The
original observed name-blue palette color remains. Same-row donors estimate the
covered name background; that region is not claimed to reconstruct hidden scenery
exactly. All palette/header/dimension/border and outside-region pixels are exact.
Every dialogue row, chat log, statistic and portrait remains unchanged.

## Native and regression verification

A fresh ordinary-input cold boot opens the actual category-two Online page. At
frame 11,300, **every one of the complete screenshot's 49,152 pixels** matches
the candidate at native five-bit RGB. All six complete glyph cells, including
blank cells and first J/last n, match: **52 ink pixels**, no missing letters.
The full native page was visually reviewed and the English name is readable.

A separate fresh New Game run chooses Prepare alone and reaches the actual Lisbon
town menu at frame 14,900. The menu, captain selection, opening story/choice and
town screen were reviewed. No callbacks fail and no savestate or memory injection
is used. Full inheritance, unchanged unowned data, golden content, focused Ruff
and exact patch reconstruction pass. There was no shared builder/runtime change.

Evidence: `work/analysis/online31_julien_v205/saved_proof.json`, `preparation.json`,
build log and exact reconstructed ROM. Native reports/frames are under
`work/emulation_v193/online31_julien_v205/`. Scripts:
`prepare_online31_julien_v205.py`, `verify_online31_julien_v205.py`.

## Primary-source search and remaining scope

The prior official Rota Nova Flash collection was already downloaded. Its 65 larger
static previews were reviewed across six sheets; they contain Rota Nova scenes,
not larger originals of the four Online screenshots. This observation was missing
from the older progress summary; the collection is not reported as newly downloaded.

The official Online guide's commented legacy link leads to `index1.htm`, which names
`bouken.swf`. Its static strings explicitly reference `image3/01.swf` through
`04.swf`. These four newly fetched publisher movies yield **81 static bitmaps**:
56 larger images and 25 small fragments, all reviewed for scene identity. They show
different tutorial screens, actors, window values and chat. No exact larger copy of
Online24/27/31/33 was found in this collection. Related interfaces do not supply the
missing original dialogue, names, values or chat. Flash/ActionScript was never run.

Two newly inspected official game images (`m_06.png`, `m_07.png`) show different
adventure/trade scenes. The linked `g_01.htm` returns 404. The higher-quality existing
`m_02.png` continues to support the four already localized Online27 bubbles; the
related character image `m_08.png` does not provide the exact Online31 transcript.
Fetch URLs, hashes, tag inventories and previews are saved under
`work/research/online_official_v205/`. Primary pages:
[publisher guide](https://www.gamecity.ne.jp/dol/guide/index1.htm),
[publisher game introduction](https://www.gamecity.ne.jp/dol/game/index.htm).

**All four screenshot bodies/chat logs remain unfinished.** The name replacement
is partial localization. The full graphics goal remains active, including remaining
name/text/caption/biography integration, legacy/archive/contextual art and broader
native/gameplay gates. V205 is not a promoted baseline or a complete translation.
User/device checks should open the Online story page and confirm normal menu/New
Game progression. At eventual completion, revisit the older record-based checks.
