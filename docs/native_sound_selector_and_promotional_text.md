# Native sound selector and promotional neighbors

## Integrated result: V130

The complete title manuscript and exact scoped tracking renderer are now registered
and integrated in experimental `all-routes-unified-v130`. All 38 title meanings and
formatting gates are reviewed for that renderer; 31 visible wordings change.
All 3,668 saved selections and 151 item owners pass, with 72 combined tests.
Promotional IDs 3289-3290 remain explicitly preserved untranslated and count as
Japanese; full source/current byte locks replace no translation requirement.
Live rendering/playback remains unverified. See the current campaign checkpoint
and `docs/common_preserved_native_neighbors.md`. Earlier sections below record
pre-integration research, including the former baseline-renderer formatting defect.

## Scoped tracking probe after title review

An isolated four-instruction BGM draw probe uses the native local tracking field
to fit all 38 complete names. All five exact-font sheets and the affected `Vol`
heading preview were reviewed; no title overflows at five-pixel advance.
**Southeast Asian Village** now occupies 115 pixels in the probe, x=7 through
x=122. All 64 combined regression tests and changed-tool Ruff checks pass.
This is a research component; V129 remains unchanged, and mixed-owner integration
plus actual runtime behavior are pending. The original six-pixel overflow remains
the reason title 3265's manuscript formatting gate is false. See
`docs/bgm_title_tracking_probe.md` for code/font locks, scope and reproduction.

## Verified loader path

Clean ARM9 file offsets use runtime address `0x02000000 + offset`.
At `0x1090D0..0x1090D4`, the constructor initializes the track selection
at object + `0x108` to 2. At `0x109268..0x109274`, the draw routine adds
literal `0xCB1` (3249, stored at `0x109308`) and calls `0x0205528C`.
That wrapper, at `0x5528C..0x552A4`, forwards to the native COMMON loader
`0x020534F4`. Thus the first track is global native message 3251. The
38-title declaration corresponds to global IDs 3251-3288. This is independent
of the original physical B36 record numbers and applies after relocation.
The track-change handler at `0x108F9C..0x109008` reads object + `0x108`,
adds the requested delta, wraps values above 39 to 2 and values below 2 to 39,
then stores the selection. This proves the static inclusive range 2-39,
corresponding to all 38 native IDs 3251-3288. When playback is active it calls
`0x020D22C0` with the selected track and then redraws. The play toggle at
`0x109008..0x10905C` uses the same track field and call; stopping calls
`0x020D2224`. This is code evidence; actual input and playback need runtime tests.
The separate volume clamp at `0x1093B4..0x1093F4` is unrelated to track bounds.

The constructor rectangle has right edge 128. The draw routine measures title
bytes at six pixels each and centers at x=64 (`0x10927C..0x1092A8`). English
BGM names should therefore be plain ASCII and no wider than 128 pixels. Safe
full-width I/F used for dialogue is not automatically appropriate for this
independent title renderer. Longer complete names require a renderer change
or faithful localization that preserves all meaning within this panel.

Disassembly and SHA-256 for the relevant clean ranges are saved in
`work/analysis/native_sound_loader_disassembly.txt`.
The event and panel-constructor ranges are saved with their hashes in
`work/analysis/native_sound_track_event_disassembly.txt`; the track-change range
SHA-256 is `6c197a402f69d63a1fc541d2b642e16a008c4810fff2b8f34561e2438c0e6773`.

## Current verification

`scripts/verify_native_sound_selector.py` verifies all 38 titles by native
message ID, all 57 accepted SFX slots, the unchanged constructor/draw/wrapper
code, track-change/play-toggle routines, and the title panel width. It checks
the canonical baseline hash and,
when supplied a profile, reviewed source-locked BGM manuscripts. It rejects a
valid shifted native start that drops a title character, changed selector
arithmetic and changed SFX text. Seven real-component regressions pass, including
changed upper/lower track limits and the play call. Six title geometry checks
also reject overflow, full-width Latin and layout/control bytes. The combined
regression suite passes all 57 tests.

The older `verify_sound_selector_build.py` checks pre-relocation physical
coordinates and is retained for historical candidates. Use the native tool
for the combined reblocked candidates. Neither tool proves title meaning,
actual selection, playback, volume or Back behavior. V129's sound report
explicitly leaves meaning review and runtime verification pending.

## Complete title manuscript: reviewed source, integration pending

`translations/common_bgm_complete_titles_v2.json` contains fresh source-locked
localizations and faithful meaning notes for every title. All five exact-font
contact sheets were visually reviewed. Thirty-seven titles fit the mapped panel;
3265, **Southeast Asian Village**, is 138 pixels wide and spans x=-5 through
x=133 in the 128-pixel panel. Its formatting gate remains false. The full name
must be accommodated by a proven renderer change. Do not remove the settlement,
abbreviate the region merely to imitate the old slot, or approve the overflow.

`scripts/prepare_common_bgm_complete_titles.py` reproduces the clean-source draft.
`scripts/audit_common_bgm_titles.py` verifies all 38 source spans, clean renderer
code, exact ASCII font and geometry. Its diagnostic panels leave overflow visible;
they are not gameplay screenshots. Evidence is in
`work/qa/common_bgm_complete_titles_v2/report.json` and all five contact sheets.
The source-owner audit independently identifies promotional neighbors 3289 and
3290: all 38 BGM titles cannot yet be integrated through the complete-owner gate.
Those neighbors must retain their full meaning and receive their own renderer
classification. This draft is unregistered, adds no shipped translation progress,
and leaves the V129 ROM, profile and canonical baseline unchanged.

| Global ID | Clean source | Reviewed proposed English |
| --- | --- | --- |
| 3251 | 勇躍 | In High Spirits |
| 3252 | エンディング | Ending |
| 3253 | 追い風に乗って | Riding the Tailwind |
| 3254 | 旅立ちのテーマ | Departure Theme |
| 3255 | 南へ行こう | Let's Head South |
| 3256 | インディアの風 | Winds of India |
| 3257 | 南海の島々 | South Sea Islands |
| 3258 | 東アジアの海 | Seas of East Asia |
| 3259 | 水平線の向こうへ | Beyond the Horizon |
| 3260 | 北欧の街 | North European Town |
| 3261 | 南欧の街 | South European Town |
| 3262 | イスラムの町 | Islamic Town |
| 3263 | アフリカの町 | African Town |
| 3264 | インドの町 | Indian Town |
| 3265 | 東南アジアの集落 | Southeast Asian Village |
| 3266 | 中国の町 | Chinese Town |
| 3267 | 日本の町 | Japanese Town |
| 3268 | 新大陸の町 | New World Town |
| 3269 | 洋上戦闘のテーマ | Naval Battle Theme |
| 3270 | 大海戦 | Great Naval Battle |
| 3271 | 海へ続く道 | The Road to the Sea |
| 3272 | 本当の宝物 | The True Treasure |
| 3273 | 波 | Waves |
| 3274 | 情熱の炎 | Flames of Passion |
| 3275 | ラファエル | Raphael |
| 3276 | ホドラム | Hodram |
| 3277 | リルとカミル | Lil & Kamil |
| 3278 | 探検！探検！ | Explore! Explore! |
| 3279 | 暗雲 | Dark Clouds |
| 3280 | 麗しの乙女 | Fair Maiden |
| 3281 | 想い | Feelings |
| 3282 | 陽気な仲間 | Merry Companions |
| 3283 | 悲しみ | Sorrow |
| 3284 | 海賊王 | The Pirate King |
| 3285 | 征服者 | The Conqueror |
| 3286 | 強敵登場 | A Mighty Foe Appears |
| 3287 | 大勝利！ | Great Victory! |
| 3288 | オープニング | Opening |

## Historical pre-V130 titles (superseded)

These historical names were replaced in V130. They show the old allocation
abbreviations; they are not the current candidate titles.

| Global ID | Clean source | Current English |
| --- | --- | --- |
| 3251 | 勇躍 | Heroic |
| 3252 | エンディング | Ending |
| 3253 | 追い風に乗って | Tailwind |
| 3254 | 旅立ちのテーマ | Set Sail |
| 3255 | 南へ行こう | Southbound |
| 3256 | インディアの風 | India Wind |
| 3257 | 南海の島々 | South Seas |
| 3258 | 東アジアの海 | E Asia Sea |
| 3259 | 水平線の向こうへ | Beyond Horizon |
| 3260 | 北欧の街 | N Europe |
| 3261 | 南欧の街 | S Europe |
| 3262 | イスラムの町 | Islam Town |
| 3263 | アフリカの町 | Africa Town |
| 3264 | インドの町 | India Town |
| 3265 | 東南アジアの集落 | SE Asia |
| 3266 | 中国の町 | China Town |
| 3267 | 日本の町 | Japan Town |
| 3268 | 新大陸の町 | New World |
| 3269 | 洋上戦闘のテーマ | Naval Battle |
| 3270 | 大海戦 | Sea War |
| 3271 | 海へ続く道 | Sea Road |
| 3272 | 本当の宝物 | True Gem |
| 3273 | 波 | Wv |
| 3274 | 情熱の炎 | Passion |
| 3275 | ラファエル | Raphael |
| 3276 | ホドラム | Hodram |
| 3277 | リルとカミル | Lil & Kamil |
| 3278 | 探検！探検！ | Explore! |
| 3279 | 暗雲 | Darkness |
| 3280 | 麗しの乙女 | Fair Maiden |
| 3281 | 想い | Feel |
| 3282 | 陽気な仲間 | Pals |
| 3283 | 悲しみ | Sorrow |
| 3284 | 海賊王 | Pirate |
| 3285 | 征服者 | Victor |
| 3286 | 強敵登場 | Foe Appears |
| 3287 | 大勝利！ | Victory! |
| 3288 | オープニング | Opening |

## Promotional owner classification still pending

## V143 BGM native title presentation

Actual BGM title centering at `0210927C` executes native strlen then uses
`64 - floor(5 * byte_length / 2)` with tracking -1 and y50. The existing generic
tracking -1 renderer dispatch draws ASCII at five-pixel advances. All 38 complete
English titles pass both native pixel formats inside the 128×160 client panel,
with exact glyph order and independent full-buffer pixels. All panels are visually
reviewed; the longest title's visible extent is x7–122. The earlier six-pixel
overflow suspicion is resolved without shortening or changing any title.

Twenty-five focused title/renderer tests and lint pass. Durable evidence:
`translations/bgm_title_native_layout_evidence_v1.json`; native sheet and detailed
report: `work/qa/bgm_native_titles_v143/`. Parent bitmap/origin setup and glyph-source
copy retain explicit diagnostic contracts. Full widget composition, physical
audio/input and cold-boot gameplay remain pending. No ROM or profile changed.

Clean B36 R63 contains BGM IDs 3286-3288 and promotional IDs 3289-3290.
The three BGM entries are already English; their Japanese source in a complete
owner queue must not be mistaken for three remaining Japanese titles.
The long body 3290 has 299 Japanese source bytes. R64 is heading 3291.
These three promotional messages remain Japanese in V129. The full clean
source and neighbors are in `work/analysis/common_b36_source_queue.json`.

The live Online overview captions have separate ARM9 strings, including
`0x16DAC4` and `0x16DA70`; accepted batches also translate Online50-62 graphics.
For example, `extras_online50_graphics_v1.json` has the captain/online-world
card. This duplication does not establish that the COMMON copies are unused.
Their callers, visibility and renderer remain unclassified. Do not exclude
them merely from an absent direct literal reference, count them complete from
a translated graphic, shorten the full body to fit a dialogue box, or relax
four-line dialogue QA without evidence of the actual presentation path.
