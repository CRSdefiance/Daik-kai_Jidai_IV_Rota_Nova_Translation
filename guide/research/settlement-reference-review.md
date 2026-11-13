# Settlement reference evidence

Recorded 2026-10-12. [Dekuno's DS password list](https://dekunobou-rotanova.seesaa.net/category/2333339-1.html) provides 24 settlement coordinates and Japanese answer associations. [Mixed-version wiki](https://w.atwiki.jp/offlinedaikoukai/pages/60.html) corroborates those coordinates and supplies service flags. The wiki's explicit PSP lodging difference prevents treating its service table as independently DS-confirmed.

English answers come from `translations/village_promised_words_manuscript_v1.json`, all 24 `ANSWER` records. `docs/village_promised_words_research_checkpoint.md` documents the case-sensitive native comparison and next-visit unlock. Sugarloaf Mountain has a space and 18 ASCII characters; preserve it exactly. The original Rio answer's trailing Japanese-space artifact was intentionally omitted by that translation work.

Export: `ds-settlement-reference.json`; builder: `build_settlement_reference.py`. Coordinate rows are DS-source-reported; facilities remain Cross-platform-unverified. Neither a source fetch nor a successful native input probe demonstrates actual travel to all settlements or every service.

Village English labels are readable guide spellings; exact live entity-name matching remains open, particularly Korfu, Forel, Leveque, and Valparaiso. The export preserves Japanese names and answer strings. Do not silently replace coordinates with modern real-world positions.

Still needed: trade goods matched to current translated commodity names, ordinary port directory, actual village service checks, map visibility/Survey mechanics, and native/runtime coordinate cross-check. No ROM or screenshot file was modified.

## Settlement goods, October 12, 2026

All 24 wiki page 60 goods mapped to existing English commodity labels. Their town associations remain mixed-version; native label existence does not verify DS stock. Alternative Ezo/Guam/Montevideo names and the explicitly PSP Golden Route guarantee are qualified.
