# Shared sailing condition names V309

Ordinary sailing in V307 showed **Admiral! 暗礁!**. The warning's reviewed
COMMON template was already English; its `%s` argument came from an untranslated
ARM9 condition-name table. The fix translates the complete26-entry table.

## Source review

Original native lookup02082E74 uses26 pointers at02148E00. Source-locked
direct callers020323A8 and02032440 pass the returned name into the original
variadic notification path02053D44. COMMON messages481–486 supply the warnings;
their original Japanese and existing English templates were inspected. Their
bytes, message IDs, speaker selection and native notification code remain intact.

| Original | English |
|---|---|
| 壊血病 | Scurvy |
| 鼠発生 | Rat Infestation |
| 嵐 | Storm |
| 吹雪 | Blizzard |
| 雨 | Rain |
| 雪 | Snow |
| 雷 | Lightning |
| 霧 | Fog |
| オーロラ | Aurora |
| 大イカ | Giant Squid |
| 化け魚 | Monster Fish |
| 鯨 | Whales |
| イルカ | Dolphins |
| セイレーン | Sirens |
| 人魚 | Mermaids |
| 謎の泡 | Strange Bubbles |
| 竜巻 | Tornado |
| 大渦潮 | Whirlpool |
| 暗礁 | Reefs |
| 流氷 | Drift Ice |
| 反乱 | Mutiny |
| 混乱 | Confusion |
| 水漏れ | Leaks |
| 伝染病 | Epidemic |
| 凪 | Calm |
| サメ | Sharks |

Names express the original sailing phenomenon. Lightning names the dangerous
weather event; Drift Ice does not invent icebergs. Leaks does not overstate
flooding. Strange Bubbles preserves the unexplained nature of the phenomenon,
and Monster Fish preserves the fantastic creature. Creature/hazard plurals work
as warning labels without asserting a specific number. None is shortened to
fit an old Japanese allocation.

## Storage and verification

All26 complete NUL-terminated English names are appended inside the existing
owned staged text pool. Original Japanese string allocations remain untouched;
only their26 table pointers change. Earlier120,000 payload bytes remain exact.
The required copy/cache wrapper and arena extent grow to120,288 bytes, leaving
8,704 bytes before the staging boundary. No unowned RAM cave is used.

Native checks execute all26 valid and four invalid selector inputs, preserve
the original fallback/stack/return behavior, and verify the complete letters
of all26 names through the game's raster code. Complete native staged-copy,
cache and arena initialization checks pass. The original selector code remains
byte-identical. Independent font pixels, bounds and buffer guards are checked.

The actual replay cold-boots V309 for30,000 frames using the same ordinary
controller/stylus schedule as the V307 discovery run through frame28800.
No savestate is loaded. Frame28800 now shows **Admiral! Reefs!** at x22,y296:
all179 ink pixels, spaces and first/internal/final letters match the game font.
All33 other comparable whole frames are exact; the201 changed pixels of the
warning frame lie exclusively inside its text box. Title/New Game, Rafael's
opening, Lisbon/departure and sailing tutorial are traversed before the warning.

This is targeted automated emulator verification. It does not certify every
condition through gameplay, complete any route or verify a physical device.
The existing six warning-template prose variants remain a separate broader
formatting/wording audit; native name rasterization is not proof of every
possible sentence produced by those templates.

## Registered experimental handoff

| Item | Identity |
|---|---|
| Candidate | `out/all_routes_combined_v309_candidate.nds` |
| ROM SHA256 | `b099a1016d08870adbdbff8693be9b5fba2f0fa611c82358bafcd507199d5289` |
| Patch | `out/all_routes_combined_v309_candidate.xdelta` |
| Patch SHA256 | `656463d795a89d7ef80f8702fc7fc174c3f648ee8cd6032714f786c2e3e55afd` |
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Canonical SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Profile | `all-routes-unified-v309` |
| Applied stack | Complete470 inherited batches, all inherited native stages, plus condition-name stage |
| Accepted layers | Retained through the immutable canonical baseline; no promotion in this checkpoint |
| Experimental change |26 shared condition labels and their owned text/copy extent |
| New changed internal component versus V307 | `/__arm9__.bin` |
| Manifest | `out/all_routes_combined_v309_candidate.manifest.json` |

Every graphics asset, route/COMMON/HELP file, ARM7, overlay and banner is exact
V307. Against the canonical base, the inherited changed internal files are:
`/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`, `/FLS/M22.fls`, `/FLS/M24.fls`,
`/FLS/M28.fls`, `/FLS/logo.fls`, `/GRP/CMMNIMG.DK4`, `/GRP/DSOBJR.DK4`,
`/GRP/SLACKIMG.DK4`, `/GRP/WINFRAME.DK4`, `/Iseki/dock.pxl`,
`/_pxl/__frame.pxl`, `/_pxl/__marker.pxl`, `/_pxl/deck04.pxl`,
`/_pxl/dividecrewinfo.pxl`, `/_pxl/logo.pxl`,
`/_pxl/mysterymap/mys_hunt_d.pxl`, `/_pxl/online/Online24.pxl`,
`/_pxl/online/Online27.pxl`, `/_pxl/online/Online31.pxl`,
`/_pxl/online/Online33.pxl`, `/_pxl/personinfo.pxl`, `/_pxl/slackimg12.pxl`,
`/_pxl/slackimg20.pxl`, `/_pxl/startmenu0.pxl`, `/_pxl/title/title03.pxl`,
`/_pxl/title/title05.pxl`, `/_pxl/winframe00.pxl`, `/data/SC0.DK4`,
`/data/SC1.DK4`, `/data/SC2.DK4`, `/data/SC3.DK4`,
`/evstill/evstill168.pxl`–`/evstill/evstill171.pxl`,
`/evstill/evstill206.pxl`–`/evstill/evstill209.pxl`, and ARM9.
The manifest lists every applied batch, stage and changed record.

The complete V307 build reproduces byte-for-byte both before and after the
optional builder stage was added. The clean-input xdelta reconstructs V309
byte-for-byte. Native selector/raster/init checks, saved-ROM inheritance and
patch checks, actual capture/font checks and Ruff pass.

Experimental; canonical unchanged and user cold-boot acceptance pending.
On the user's emulator, check title/New Game, Rafael's opening/town, departure
and the sailing warnings when encountered. Broader condition contexts remain
open, rather than requiring the user to manufacture every random phenomenon.

## Remaining graphics goal

No weapon/armor was acquired in this voyage. All18 ongoing plaque/hint entries
and their Armor/Weapon variants remain incomplete in both authoritative audits.
Actual alternate conditions, occupied weapon/armor, legacy raw graphics consumer
and crop checks, hidden Gallery contexts and final full-goal audit remain open.
Low resolution Online screenshots remain exempt by user instruction; inherited
partial edits are preserved.

The [item-location walkthrough](https://w.atwiki.jp/offlinedaikoukai/pages/81.html)
lists Golden Cutlass in Istanbul. This is a multi-version acquisition lead,
not confirmation of a DS purchase or credit toward occupied equipment.
The voyage's ordinary-input captures and report are retained separately.

Evidence: `work/analysis/sailing_conditions_v309/native_proof.json`,
`native_selector_callers.json`, `release_proof.json`, the two V307 reproduction
ROMs, and `work/emulation_v193/sailing_conditions_v309/capture_report.json`.
Revisit older record-based checks at actual full-goal completion.
