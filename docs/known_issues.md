# Known issues

## Packaged combined V89 candidate

All routes are packaged in `releases/all_routes_unified_v89/translation.xdelta`.
Four older Lil literal percentages in B128R0268/R0311/R0317 and B164R0140 were
rewritten to avoid native printf commands. Their source meanings, controls,
macros, automatic wrapping and leading characters were reviewed and audited.
The package has its own current checksums and verification reports; the earlier
Lil V123 checkpoint checksum describes the historical pre-repair candidate.
Runtime cold-boot testing and release acceptance remain pending.

## Complete Lil translation, experimental combined V123 candidate

Lil translation coverage is complete: 6,539 translated, zero remaining and
69 native controls preserved. Final 77 scene texts and B22 control classification
pass eight-sheet review, zero-blocker audit, 77 Lil tests, Ruff, baseline and
exact saved-ROM verification. All four routes are combined. Runtime gameplay
and release acceptance remain pending; this does not claim emulator verification.
See `docs/all_routes_unified_lil_v123_checkpoint.md`.

## Experimental four-route Lil V121 candidate

B324 adds 59 verified jungle records; three packed events unchanged.
Six sheets, QA, 75 Lil tests, Ruff, baseline and saved-ROM checks pass.
Coverage 6,408/6,608; 137 remaining; 63 excluded. Continue B325. Runtime pending.
See `docs/all_routes_unified_lil_v121_checkpoint.md`.

## Experimental four-route Lil V120 candidate

B323 adds 66 verified fog records; four packed events unchanged.
Seven sheets, QA, 74 Lil tests, Ruff, baseline and saved-ROM checks pass.
Coverage 6,349/6,608; 199 remaining; 60 excluded. Continue B324. Runtime pending.
See `docs/all_routes_unified_lil_v120_checkpoint.md`.

## Experimental four-route Lil V119 candidate

B317-B319 adds 35 verified fortune/trade texts after 94 scorpion texts in V118.
Four sheets, QA, 73 Lil tests, Ruff, baseline and saved-ROM checks pass.
Coverage 6,283/6,608; 269 remaining; 56 excluded. Continue B323. Runtime pending.
See `docs/all_routes_unified_lil_v119_checkpoint.md` and V118 checkpoint.

## Experimental four-route Lil V117 candidate

B314-B315 adds 38 verified forest/map records; two packed events unchanged.
Four sheets, QA, 71 Lil tests, Ruff, baseline and saved-ROM checks pass.
Coverage 6,154/6,608; 398 remaining; 56 excluded. Continue B316. Runtime pending.
See `docs/all_routes_unified_lil_v117_checkpoint.md`.

## Experimental four-route Lil V116 candidate

B312-B313 adds 84 verified wolf/gate records; two packed events unchanged.
Nine sheets, QA, 70 Lil tests, Ruff, baseline and saved-ROM checks pass.
Coverage 6,116/6,608; 438 remaining; 54 excluded. Continue B314. Runtime pending.
See `docs/all_routes_unified_lil_v116_checkpoint.md`.

## Experimental four-route Lil V115 candidate

B307-B311 plus B306R0081 adds 44 verified temple/Proof records. Five sheets,
QA, 69 Lil tests, Ruff, baseline and saved-ROM checks pass. Coverage
6,032/6,608; 524 remaining; 52 excluded. Continue B312. Runtime pending.
See `docs/all_routes_unified_lil_v115_checkpoint.md`.

## Experimental four-route Lil V114 candidate

B306 adds 39 river records and two unchanged packed events. Four sheets,
QA, 68 Lil tests, Ruff, baseline and saved-ROM checks pass. Bare Japanese
97AC variant follows in V115. Coverage 5,988/6,608; 568 remaining; 52 excluded.
See `docs/all_routes_unified_lil_v114_checkpoint.md`. Runtime pending.

## Experimental four-route Lil V113 candidate

B301-B305 adds 85 verified desert and Basra quest records. Nine sheets,
QA, 67 Lil tests, Ruff, baseline and saved-ROM checks pass. Coverage
5,949/6,608; 609 remaining; 50 excluded. Continue B306. Runtime pending.
See `docs/all_routes_unified_lil_v113_checkpoint.md`.

## Experimental four-route Lil V112 candidate

B299-B300 adds 103 verified snake/bog records; one packed event unchanged.
11 sheets, QA, 66 Lil tests, Ruff, baseline and saved-ROM checks pass.
Coverage 5,864/6,608; 694 remaining; 50 excluded. Continue B301. Runtime pending.
See `docs/all_routes_unified_lil_v112_checkpoint.md`.

## Experimental four-route Lil V111 candidate

B295-B298 adds 23 verified wristband quest records. Three sheets, QA,
65 Lil tests, Ruff, baseline and saved-ROM checks pass. Coverage 5,761/6,608;
798 remaining; 49 excluded. Continue B299. Runtime pending.
See `docs/all_routes_unified_lil_v111_checkpoint.md`.

## Experimental four-route Lil V110 candidate

B293-B294 adds 98 verified fog/cliff records; two packed events remain
unchanged. Ten sheets, QA, 64 Lil tests, Ruff, baseline and saved-ROM checks
pass. Coverage 5,738/6,608; 821 remaining; 49 excluded. Continue B295.
Runtime pending. See `docs/all_routes_unified_lil_v110_checkpoint.md`.

## Experimental four-route Lil V109 candidate

B289-B292 adds 51 verified Angkor riddle records; two packed events remain
unchanged. Six sheets, QA, 63 Lil tests, Ruff, baseline and saved-ROM checks
pass. Coverage 5,640/6,608; 921 remaining; 47 excluded. Continue B293.
Runtime pending. See `docs/all_routes_unified_lil_v109_checkpoint.md`.

## Experimental four-route Lil V108 candidate

B288 adds 82 verified cave encounter records. Nine sheets, QA, 62 Lil tests,
Ruff, baseline and saved-ROM checks pass. Coverage 5,589/6,608;
974 remaining; 45 excluded. Continue B289. Runtime pending.
See `docs/all_routes_unified_lil_v108_checkpoint.md`.

## Experimental four-route Lil V107 candidate

B283-B287 adds 104 verified natural-English forest and wine-delivery records;
one corroborated packed event remains unchanged. All 11 sheets, QA, 61 Lil
tests, Ruff, baseline and saved-ROM checks pass. Coverage 5,507/6,608;
1,056 remaining; 45 excluded. Continue B288. Runtime pending.
See `docs/all_routes_unified_lil_v107_checkpoint.md`.

## Experimental four-route Lil V106 candidate

B255-B282 adds 154 verified natural-English guild quest records. All 16
sheets, QA, 60 Lil tests, Ruff, baseline and saved-ROM checks pass.
Coverage 5,403/6,608; 1,161 remaining; 44 excluded. Continue B283.
See `docs/all_routes_unified_lil_v106_checkpoint.md`. Runtime pending.

## Accepted cumulative Lil/Guild/Hodram V1 baseline

The user explicitly promoted `out/lil_hodram_unified_v1_candidate.nds` on
2026-09-17. Its bytes are now the canonical
`out/raphael_natural_v2_accepted_base.nds`; the SHA-256 is
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
The former canonical baseline is retained as
`out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds`,
SHA-256 `0c6e5a686b4fefb98a4d25ebb3c0e8c90ffa20e3f43240ca1629d8f6d40c85f2`.
The promotion bakes Lil's 49-record Amsterdam opening, shared name and fleet
repairs, Guild and Inn UI, all 218 item names, the Amsterdam Guild item
descriptions, and the cumulative Hodram, market, shipyard, cargo, Inn, and
at-sea repairs. The manifest passed every release check and the full regression
suite passes (346 tests).

## Accepted Raphael Story V10 baseline

The user explicitly promoted `out/raphael_story_push_v10_candidate.nds` on
2026-09-09. Its bytes are now the canonical
`out/raphael_natural_v2_accepted_base.nds`; the SHA-256 is
`0c6e5a686b4fefb98a4d25ebb3c0e8c90ffa20e3f43240ca1629d8f6d40c85f2`.
The former canonical baseline is retained as
`out/raphael_natural_v2_pre_story_push_v10_accepted_rollback.nds`, SHA-256
`d8cb15aa23e2496510eba8feb18e4536a7da195522b7f5959298b0c1cc0fd1cf`.
The V10 manifest and independent baseline and Sound verifiers cover the
accepted integrated layers. The full regression suite passes (282 tests).

The profile adds 1,257 safe translated records across COMMON blocks 15-40,
including 580 records in blocks 22-40. Every record in blocks 22-40 is
classified as buildable English, an explicitly blocked packed/macro/identifier
or renderer-constrained draft, or padding-only. No placeholder filler is used.

Promotion does not make every packed entry playable in English. Records with
unmapped interior entry points, the packed BGM/promotional tables, internal
scene identifiers, ambiguous `{MACRO:I}C` sequences, and drafts that overflow
or destabilize the progressive renderer remain byte-identical to Japanese.
They are retained in the corresponding `*_blocked.json` inventories for the
next translation phase.

## Integrated trade, crew, and Deck View layer (accepted and baked)

`out/raphael_story_push_v10_candidate.nds`, SHA-256
`0c6e5a686b4fefb98a4d25ebb3c0e8c90ffa20e3f43240ca1629d8f6d40c85f2`,
is the promoted source build. Its changes are baked into the canonical parent.
It replaces the clipped trade-screen
`Confirm` caption with the pair-safe `Select`, repairs the trader greeting and
investment prompt, and translates the generic sailor nameplate.

The city-information screen now uses source-derived textured plaques with
native-font `Type`, `Status`, `Growth`, `Arms`, `Share`, and `Specialty`
captions. The fixed `Prt` abbreviation is now `Port`; its adjacent `City`
string was safely moved by one byte and its runtime pointer retargeted. All 19
live cultural-region entries are verified English, covering German, Nordic,
Portugal, Spain, Italy, Greece, Turkey, Egypt, West Africa, East Africa, Arab,
India, Indochina, Indonesia, China, Korea, Japan, Caribbean, and Mexico. The
port market's Japanese category header is redrawn as `Type` and `Market %`.

Assign Sailors now restores each complete accepted plaque before drawing a
centered native-font caption. Its terminology is consistent with Ships:
`Fleet Crew`, `Unassigned`, `Range`, `Marines`, `Cannon`, `Lateen`, and
`Square`. The former `~%d d` range formatter, whose tilde resembled a stray
dash, is now the unambiguous `%d days`.

Deck View now translates the full compact room table (`Cabin`, `Helm`,
`Survey`, `Mast`, `Galley`, `Sickbay`, `Purser`, `Tactics`, `Chapel`, and the
remaining room states), both requirement-label variants, all assignment
eligibility/restriction messages, and the compact ability-name table. The
captain-cabin warning is `Only %s can be Captain.` and the generic warning is
`Cannot assign here.` The Y button is now `Crew`, matching the automatic
Explore/Trade/Battle crew-policy menu it opens instead of the clipped
`Staff`/`Stat` wording. The policy confirmation now reads `Confirm crew
assignment?`; its adjacent empty-roster warning and captain requirement read
`No unassigned crew.` and `Command`.

The selected-character activity panel has a measured hard limit of 24
single-byte glyphs and does not wrap. Seventy-one accepted COMMON B17 activity
responses exceeded that limit; every one now uses a complete, renderer-safe
sentence of at most 24 glyphs. This repairs the photographed wheel and captain
lines and prevents equivalent truncation in cooking, prayer, strategy,
accounting, surveying, lookout, sail-handling, marine, and gun-deck responses.
The 59 activity lines that already fit remain from the accepted B17
localization; for example, `Test-firing now.` is the complete translation of
`只今／試し撃ちをしています`, not placeholder text. One player-facing B17
record inherited the literal early-pass placeholder `see below`; V10 replaces
it with the context-faithful `Leave diplomacy to me.` Thus all 132 Deck
activity records are now English; padding-only record 132 is not dialogue.

The release builder also rejects legacy SC0-SC3 translations and every story
profile that cannot prove guarded line breaks and ASCII pair parity. This turns
the known dropped-first-glyph failure into a build-time invariant. New routes
still require one route-level mapping of presentation bytes and macro expansion
lengths before their dialogue can pass the gate.

The candidate passes all 282 automated tests, the accepted-baseline invariant
check, and the independent Sound-selector verifier (38 BGM and 57 SFX titles).
Cold-boot it and review the trader greeting, investment flow, trade bottom
buttons, sailor confirmation, city Type/Status panel, port information in
several regions, and every Assign Sailors label/value pair. In Deck View,
cycle through every room, press Y on several navigators, attempt an invalid
room assignment and the captain cabin, then assign several characters across
different duties to sample the shortened activity responses. The user reviewed
the evolving builds through supplied cold-boot screenshots and explicitly
promoted V10 on 2026-09-09; the profile is now `accepted-baked`.

## Route-map cities and Forces patch (accepted and baked)

`out/ships_route_forces_v1_candidate.nds` is the historical component review build.
Its SHA-256 is
`f7edd035b4471da221f5701fae224c824065fe75fa86904a4982b9bfcb7a9c6b`.
It is built from the canonical accepted baseline under profile
`ships-route-forces-v1` and changes only `/__arm9__.bin`,
`/_pxl/forceinfo.pxl`, and `/_pxl/shipinfo.pxl`.

The route-map audit now follows the game's actual 113 city objects and their
runtime name pointers. Every live target is ASCII, null-terminated, and checked
against an ordered English inventory. This catches alternate copies such as the
previously missed Hamburg string and exact-width names such as Hangzhou,
Nagasaki, and Tsukushi. The map coordinate format now begins with a protected
line break so Amsterdam renders its name on the first line and `N 52 E 5` on the
second instead of producing `AmsterdamN`.

The Forces screen restores clean source-derived backgrounds for the original
textured `Level` plaque and four folded-ribbon `Funds`, `Power`, `Home`, and
`Ties` labels before drawing native-font English. It does not replace their
artwork with flat rectangles. Its leader role, unknown-force heading, all eight
region names, and the previously missed Hayreddin, Silveira, Uddin, and
Centurione force names are English. Both live copies of the bottom X-button are
translated, yielding pair-safe `Area`, `Map`, and `Back` buttons. All 189
profiled sailor-name records in the accepted base are verified ASCII. The
candidate also includes the pending Ships V2 refinements described below.

The linked World Map area-selection screen is translated across all of its
runtime variants: `World Map`, `Area: select one.`, `Press X to change selection
type.`, and the alternate `Fleet/Town` target. Its bottom captions are now
`Switch`, `Area`, `Back`, and `Done`; duplicate Switch/Done slots are patched so
the wording remains English as the selection mode changes.

The component was accepted as part of the promoted V10 baseline. For regression
testing, inspect route-map cities in Europe and several other
regions, including Hamburg, Amsterdam, Hangzhou, Quanzhou, Nagasaki, and
Tsukushi. Confirm the top title and map bubble are English, coordinates occupy a
clean second line, and all three bottom buttons render fully. Open Forces and
confirm the leader role, unknown-force heading, regional power name, five
textured plaques, the four newly repaired force names, and Area/Map/Back
buttons. Open the World Map and switch between Area and Fleet/Town, checking the
title, all three instruction lines, and Switch/Area/Back/Done captions. Then
repeat the Ships V2 checks. The profile is now `accepted-baked`.

## Opening-movie patch (accepted and baked)

`out/opening_movie_v1_candidate.nds`, SHA-256
`88255d2b2280ff4e3956124106e7b866ba68bbc92bc838b2f0b5bf08be87d3b3`,
extends the Ships/route/Forces review build under profile `opening-movie-v1`.
It translates both cyan title overlays (`Press START or touch the screen` and
`Press A or touch the screen to skip`) and the previously missed M20 subtitle
(`What is it, Clau? / What did you want to show?`). The M20 card is
laid out within its proven 168-pixel live viewport rather than its 256-pixel
storage allocation, preventing the right edge from being cropped in-game.

All five M20/M22/M24 movie subtitle cards are rebuilt with the source format's
three distinct palette roles: transparent background, opaque black outline, and
white fill. This corrects the thin outline-free English cards in the accepted
baseline without changing animation data, illustrated frames, archive sizes, or
any unrelated file. The candidate passes all 266 tests plus the independent
baseline and complete Sound-selector verifiers.

The component was accepted as part of the promoted V10 baseline. For regression
testing, let the opening movie play without skipping and confirm
the cyan Start/touch and A/touch prompts are centered and legible, the Clau line is
English, and every English white subtitle has a solid black edge over both pale and
dark artwork. Then start each available captain once and confirm the opening-name
animations and route transitions remain intact. The profile is now
`accepted-baked`.

## Ships submenu patch (accepted and baked)

The first cold-boot review confirmed the native captions, English `Cpt.`, and
`Culverin 24` spacing. It also established that the two dark tiles beside the
contents label are the game's native cargo-item thumbnails and that the slanted
tile before `Culverin` is its native cannon thumbnail. V2 retains those runtime
sprites and the complete source plaques, changes `Goods` to the clearer `Cargo`,
and replaces the overly specific `Lateen` with the accurate `Fore/Aft`.

`out/ships_submenu_v2_candidate.nds` is the historical component review build. Its SHA-256 is
`ed980cc03a0aeae8823f04bac4bfd7f55aae4528140d8b7f96862b02ed81509a`.
It is built from the canonical accepted baseline under profile
`ships-submenu-v2`, changes only `/__arm9__.bin` and `/_pxl/shipinfo.pxl`, passes
all 258 tests, and passes the independent baseline and Sound selector verifiers.

`out/ships_submenu_v1_candidate.nds` rebuilds the Ships information panel from
the accepted baseline under profile `ships-submenu-v1`. Its SHA-256 is
`5a36502dcd7dcb7682c91b87f33618ba4d4f99f0568f12bcc1f515d137bfdc8c`.
Only `/__arm9__.bin` and `/_pxl/shipinfo.pxl` change.

The eleven beige panel captions now use DK4's native bitmap font. Terminology
has been corrected from the ambiguous `Cargo`, `Load`, and `Sail` to `Holds`,
`Goods`, and `Lateen`; the remaining labels are `Water`, `Food`, `Crew`,
`Square`, `Marines`, `Guns`, `Cannon`, and `Hull`. `Goods` and `Cannon` are
drawn only within the safe left portions of their source plaques, leaving the
runtime cargo and cannon icon zones clean. Three `%s艦長` formats now render as
`%s Cpt.`, and the fixed Culverin name carries a trailing separator before its
runtime value.

Cold-boot the candidate, open Common > Info > Ships, and inspect ships with
filled goods slots, both sail types, marines, guns, and a Culverin. Confirm the
two goods icons and cannon icon are unobstructed, `Culverin 24` is separated,
the captain suffix is English, every numeric value remains aligned, ship
selection still works, and Back returns normally. Keep this layer experimental
until those runtime overlays are confirmed.

## Extras, Options, Sound, and Common-menu layer (accepted and baked)

`out/extras_options_sound_common_v6_candidate.nds` is the corrected Extras,
Options, Sound Setup, and Common-menu candidate. Its SHA-256 is
`d8cb15aa23e2496510eba8feb18e4536a7da195522b7f5959298b0c1cc0fd1cf`.
It is built from the promoted canonical baseline under profile
`extras-options-sound-v1` and changes only ARM9, COMMON MESFILE blocks 4 and 36,
`/GRP/DSOBJ.DK4`, `/_pxl/dividecrewinfo.pxl`, and the fourteen declared Online
PXL resources.

The live text pass covers both Extras root choices; Overview, Careers, First
Steps, and Create a Story; all feature captions; the tie-in explanation, two
instruction steps, village details, service notice, and closing page. The
graphics pass redraws the Online banner and all thirteen baked Japanese text
cards with an opaque dark outline for legibility over the transparent scenic
background. Stored multiline pages use pair-phase-safe protected breaks so the
first glyph of each line remains in place, and all Previous/Next variants are
English. The title label now uses the complete `Options` spelling. The Sailing
Help prompt owns its full source range instead of leaving `現在` behind; both
Options prompts use coherent On/Off language while retaining the renderer-safe
full-width Latin workaround.
Promotional gameplay screenshots remain historical source images and
are not altered merely because tiny Japanese UI is visible inside them.

The Sound layer was rebased as a coordinated unit: all 38 packed BGM titles,
their interior pointer table, and all 57 SFX titles. The independent Sound
verifier passes, but playback behavior remains a cold-boot gate.

V1 translated the standalone marker atlas but missed the live town sprites. V2
then synchronized the matching copy in CMMNIMG block 5, but a full emulator
restart proved that block is archival: the wheel still remained Japanese. V3
identified the correct `/GRP/DSOBJ.DK4` sprites, but copying complete marker
strips damaged the frames and retained poor source lettering. V4 instead keeps
the original OBJ art, reconstructs only the Japanese glyph pixels from the six
repeated button backgrounds, and draws crisp English with DK4's native bitmap
font. Every padding row and unrelated tile is preserved. The earlier cache,
CMMN runtime-source, and full-strip-copy approaches are revoked.

V5 extends that repair through the Common-menu children. It translates the
Info and Functions choices plus the related report and docked-ship entries,
replaces the complete Japanese Deck View help paragraph, and shortens the
screen heading to `Deck` so its final glyph cannot be clipped. The seven
Assign Sailors plaques are redrawn with the same native 5-pixel-spaced game
font; pixels outside their declared label boxes are byte-identical.

V6 completes the Common Functions cleanup visible in the latest review. Save
and Load now have English screen titles, `Unused`, `At Sea`/`Docked` status,
level format, confirmations, progress notices, and read/write errors. Common
Options uses `Reports`—the same term as the main-menu Options screen—instead
of the contextually incorrect `Finances`, and `Sail Help` replaces the final
Japanese child label. The empty-inventory Items route now says `You have no
items.` without the erroneous `%s` formatter that previously consumed stray
memory and displayed a Japanese glyph.

Cold-boot the candidate and traverse every Extras and Options branch before promotion.
Check menu selection, wrapping, page order, Next/Back behavior, banner quality,
every Online text card, every BGM/SFX entry, playback, volume control, and all
Common radial-menu entries in town. The user approved V6 on 2026-09-03; all of
these layers are now baked into the canonical baseline and inherited by future
playable builds.

## Interface-polish layer (accepted and baked)

`out/interface_polish_v1_candidate.nds` was the interface-first test candidate.
Its historical SHA-256 is
`469f4ac97354d36f96bb5d5a05a3deac1c246edcb2f24b7277e6b0296f7bdc36`.
The `interface-polish-v1` profile is now accepted and baked into the canonical
baseline promoted on 2026-08-31.

The ARM9 interface audit covers all 810 mapped fixed slots: 804 contain their
exact profile text and six contain an accepted English variant. No Japanese
slot or uncovered high-confidence ARM9 scan hit remains. The covered tables
include character names, ship models, commodities, cities, settlements,
factions, trade categories, roles, buttons, and compact menu fields.

This candidate also translates the 18 remaining captions in the shared marker
atlas, the standalone Confirm, Distributed Goods, Spoils, and Temporary
Storage strips, and polishes the regional-fleet, force, town-info, and Golden
Route panels. These are graphical edits, so a warm-loaded emulator can continue
showing cached Japanese tiles; test from a full emulator restart.

Known interface limits remain: the naming keyboard opens on its Japanese page
and its `英`/`記` identifiers are functional data rather than safe captions; the
town HUD month/day suffixes use an unadapted low-level renderer; and a few
strict fixed slots require readable abbreviations. The original Japanese title
logo is retained as branding. A post-promotion cold-boot smoke pass remains useful.

## Hodram trading-complete layer (accepted and baked)

`out/hodram_trading_complete_candidate_v1.nds` was the integrated experimental
candidate for the Stockholm/Lubeck trading and tavern pass. Its historical SHA-256 is
`238151a3ae9f092da906640db0f47b1d0aaac78bbccb74520df860ee32699e9e`.
The corresponding profile is now accepted and baked into the promoted baseline.
The historical candidate changed only
`/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/towninfo.pxl`, and
`/data/SC1.DK4`; the independent baseline verifier passes.

The candidate repairs the packed trader and tavern entry points that caused
dropped initial letters, empty boxes, and dialogue tails. It also terminates
the fixed-width commodity strings that produced `Iron OreLiFam`, shortens
clipped trading buttons, translates the mapped Lubeck port/region/faction
fields, and redraws the four compact town-info captions at a readable size.

The compact Japanese trading captions visible in the cargo/category panels were
subsequently mapped to the shared marker atlas and standalone PXL strips. Their
English redraws are included in the promoted baseline. A warm-loaded emulator can
retain the old tiles, so verify them after a full restart.

## Runtime-owned ARM9 tail falsely identified as code caves

Nothing in `0x02171E48` through `0x02172463` may be used for code, flags, or
temporary storage. Although that range is zero-filled in the ROM's ARM9 image,
it is runtime-owned data:

- the known-good Raphael savestate contains structured values at
  `0x02172300` through `0x0217231F`;
- the cold-boot New Game trace contains structured values at
  `0x021723FC` through `0x02172463`; and
- the supposed flag at `0x021723FC` held `E0`, enabling old helpers during New
  Game initialization.

The old helpers overwrote this live data, which explains the freeze before
Choose Captain. Register preservation and the `BL` link register were not the
underlying cause. `scripts/build_protected_newline_renderer_probe.py` and
`scripts/build_register_safe_dialogue_cursor_probe.py` now hard-fail before
writing a ROM.

The exact baseline remains `out/dialogue_live_safe_v3.nds`, SHA-256
`baf77c53beed5a681452517c45391cb7b3c9230ccf9a593feb82a6eede6e53ce`.
It reaches Choose Captain but retains the safe one-cell continuation indent.

## Blocked stateless guard-skip hook at `0x020D550C`

The original instruction at `0x020D550C` is `01 90 89 E2`
(`add r9, r9, #1`). New Game executes this shared LF path twice, from
`LR=0x020D59DC`, with the LF followed by ASCII `A` and `R`; it executes zero
Raphael story-wrapper calls. A stateless helper could preserve those cases by
advancing one byte unless the following byte is ASCII space.

However, the proposed helper address `0x02172300` is proven live data, so no
such ROM was built. Do not patch `0x020D550C` until the helper has a separately
verified executable location or a cave-free relocation design. ROM zeros alone
are never sufficient evidence of a cave.

### Revoked cave-free inline guard-skip probe

`out/dialogue_guard_skip_inline_probe.nds` replaces only the existing LF bounds
decision block at runtime `0x020D5504` through `0x020D556B`. It uses no helper,
flag, code cave, or external storage. The rewrite advances `r9` by two only for
`LF+SPACE`, advances by one otherwise, preserves the original four signed bounds
checks, restores the original successful-path register state, and branches only
to the original `0x020D57FC` and `0x020D5808` targets.

- Base: `out/dialogue_live_safe_v3.nds`
- Base SHA-256: `baf77c53beed5a681452517c45391cb7b3c9230ccf9a593feb82a6eede6e53ce`
- Probe SHA-256: `52b5acbd4e556a02caed114fbee54d82abd9cac6f1a1288ce9f1c7f460988ab7`
- Changed component: `/__arm9__.bin`
- Changed ROM file range: `0x000D9504` through `0x000D956B`

Cold-boot testing rejected this candidate. It reached Raphael dialogue, but the
first continuation glyph moved to the end of the preceding line in every tested
stored break:

- `Ah, now` rendered as `Ah.n` followed by `ow`;
- `Behold` rendered with `B` at the end of line one and `ehold` on line two; and
- `when we` rendered with `w` at the end of line one and `e have` on line two.

The flush-left second line in `She was a wreck when we got her. / Janus helped
rebuild her.` is not contrary evidence: it is an automatic word wrap rather
than a stored protected `LF+SPACE` boundary, so the guard-skip path is not used.

This proves that the progressive renderer needs the guard byte for display
timing, not merely pointer advancement. The candidate is revoked and must not
be distributed or used as a parent. Its builder now hard-fails.

### Guard-preserving inline cursor probe awaiting cold-boot test

The follow-up trace recorded the complete protected transition four times:
LF processing reset the horizontal cursor to `0`, the stored guard space was
processed normally, and the first real continuation glyph began with cursor
`6`. This confirms the indent is exactly the guard's six-pixel advance.

`out/dialogue_guard_cursor_inline_probe.nds` preserves the LF and guard-space
source advancement. Immediately before the first glyph after an exact `0A 20`
sequence, it changes the cursor from `6` to `0`. It does nothing unless both the
byte history and traced cursor value match, uses no external storage or code
cave, and leaves automatic wrapping unchanged.

- Base: `out/dialogue_live_safe_v3.nds`
- Base SHA-256: `baf77c53beed5a681452517c45391cb7b3c9230ccf9a593feb82a6eede6e53ce`
- Probe SHA-256: `74b8a63f5b87ba7f231ff19c869a4c01eb7a9194ab3c5444839ae89839cdde98`
- Changed runtime ranges: `0x020D5504` through `0x020D556B`, and
  `0x020D5804` through `0x020D5807`

Cold-boot testing showed that the stored wraps were otherwise correct, but the
uppercase `J` in `Janus` disappeared when drawn at cursor zero. The following
`anus` remained one cell later. This candidate is revoked; do not use it as a
parent. The next candidate retains a one-pixel left inset to keep glyph ink
inside the dialogue clip rectangle.

`out/dialogue_guard_cursor_one_pixel_probe.nds` is that experimental follow-up.
It differs only by storing cursor `1` instead of `0` after the proven
`0A 20` / cursor-`6` condition.

The first glyph-draw trace of this failure was inconclusive because a broad
space/`J`/`a` filter exhausted its event limit before reaching the protected
`Janus` line. The only captured `J` had unrelated source context `00 00 4A 75`.
The narrowed trace must capture exact source sequence `0A 20 4A 61 6E` before
any further renderer ROM is built.

That narrowed trace subsequently proved that glyph `0x4A` is submitted to the
virtual draw call at `0x020D5774` with cursor `1`; glyph `a` follows at cursor
`7`. Thus the missing letter is not consumed or skipped by the source loop. It
is rejected or clipped inside the virtual drawing implementation. Identify the
runtime `r3` callback and its left-boundary logic before designing another ROM.

The next trace identified that callback as `0x020D4DA8`. The embedded `J` bitmap
is valid (`00 00 10 10 10 10 10 10 90 90 60`), so a blank font cell is not the
cause. A static vtable match incorrectly suggested inner target `0x020D4FC8`;
live execution did not enter it. The pending ASCII-pair dispatch is
`0x020D4FA4`, and the actual inner target must be read from the live object's
`[vtable+0x20]`. Capture that target and pair rectangle before patching any
shared drawing routine.

Live execution confirmed vtable `0x021603E4` and inner target `0x020D4FC8`.
Because ASCII is batched in pairs, the protected `J` may occupy either byte;
diagnostic filters must accept both `[J, a]` and `[space, J]` rather than assume
the first position.

The corrected capture proved the batch is `[space, J, NUL]` at rectangle
`(x=0, y=12)`. `J` is drawn in the second cell at `x=6`; cursor compensation
then places `a` at `x=6` or `x=7`, overwriting the `J`. The disposable
`out/dialogue_guard_pair_phase_probe.nds` flips only record 71's pair phase with
an invisible pre-LF space and changes `rebuild` to `repair` to preserve the
exact 60-byte allocation. It is experimental until cold-boot tested.

Cold-boot testing passed for SHA-256
`265ee31b6a629f139f7745a0cda8b0178cf5ec4a3faef58b647986202746cc07`.
The user confirmed the ROM worked and the complete `Janus` line rendered. This
validates the pair-phase repair, but the disposable probe is not yet the
canonical integrated baseline.

- Base SHA-256: `baf77c53beed5a681452517c45391cb7b3c9230ccf9a593feb82a6eede6e53ce`
- Probe SHA-256: `289bc1d1d60b16daee69469d277c128b0ccf09b4a5e49cf1b2625375166c4040`
- Changed runtime ranges: `0x020D5504` through `0x020D556B`, and
  `0x020D5804` through `0x020D5807`

Cold-boot testing also rejected this candidate: the uppercase `J` was still
missing. This disproves the simple left-edge clipping hypothesis. Both cursor
variants and their builder are revoked. Do not try further cursor offsets
without tracing the actual single-byte glyph draw call.

## Prohibited global cursor hook: `0x020D5504`

Do not apply newline cursor compensation globally at ARM9 `0x020D5504`. Although
the progressive story trace proved that the guard is drawn from this routine, the
routine is shared with New Game/menu transition rendering. The tested cursor
probe left the pointer contract intact but still broke immediately after New Game
while audio continued. A future experiment must be caller-scoped to the standard
dialogue call returning to `0x02054928`; otherwise retain the safe one-cell indent.

### Revoked first caller-scoped probe

`out/dialogue_scoped_cursor_probe.nds` is a disposable test ROM, not a release
base. It enables compensation only around the standard-dialogue call at
`0x02054924`. Test it from a full emulator restart without a savestate:

1. Confirm the title menu appears and Options still opens.
2. Select New Game and confirm Choose Captain appears and remains responsive.
3. Start Raphael and reach Claudio's `Prince Henry and Duke Leon` line.
4. Capture that line, `Behold, the Carteira!`, and `Not right away...`.

Any freeze, missing menu, altered portrait/speaker, dropped first glyph, split
word, or regression outside those continuation lines revokes the probe.

The first probe was revoked on 2026-08-12. Options remained functional, but
selecting New Game removed the menu, left the title background visible, and
stopped responding while music continued.

The subsequent read-only comparison trace changed the diagnosis. During the
entire failing New Game transition it recorded **zero** executions of the
`0x02054924` call (`calls=0`). The two observed LF events belonged to another
renderer path returning to `0x020D57E4`. New Game therefore did not enter the
story wrapper. The initial register-clobber hypothesis was later superseded by
the cave-safety trace described above.

The attempted register-preserving correction,
`out/dialogue_register_safe_cursor_probe.nds`, was also revoked by cold-boot
testing: New Game froze before Choose Captain. Its helper preserved `r12`, but
it overwrote runtime-owned data at `0x021723FC` through `0x02172463`.
Never reintroduce either earlier helper or reuse any address in the blocked tail.

## Options report and sailing-help prompt encoding

The Options confirmation prompts live in `__arm9__.bin`, but they are rendered by a
fixed-width Shift-JIS dialog path rather than the normal ASCII-capable menu renderer.
The original `options_menu_en.nds` inserted ASCII into those slots and is revoked: the
resulting text was visibly mangled (`Income reports` and `Sailing help`).

`out/options_menu_v2.nds` is the corrected research candidate. Its two prompts use
CP932 full-width Latin characters, retain the original `%s` substitutions, and are
built directly from `out/all_goods_roundtrip.nds`. Do not replace text in either
prompt with ASCII. Any future revision must retain the exact source-byte lock and be
cold-boot tested before promotion.

The scrolling BGM/SFX labels are not the same ARM9 caption table. They are now
mapped and translated in `out/extras_options_sound_v1_candidate.nds`:
38 BGM titles are packed across `/COMMON/MESFILE.DK4` block 36 records 46-63,
while 57 SFX titles occupy fixed or standalone ARM9 slots. The BGM panel uses a
packed interior-pointer table; replacing labels without remapping those pointers
produces fragmented and reordered words. V1 through V3 are therefore superseded.
V4 correctly remapped the titles but is revoked because its build command omitted the
accepted Options/UI batch, reverting the surrounding menu. V5 is superseded. The
current `sound-setup` batches are source-locked to the accepted Raphael baseline and
must still be applied together. Some titles remain abbreviated to fit their original
packed regions. The combined candidate passes structural and pointer verification;
keep it experimental until every title, selection, playback, volume, and Back path is
cold-boot tested.

## Lil opening scene control preamble

Lil's actual opening is `/data/SC2.DK4`, block 22. Its dialogue records begin
with control sequences that affect the active portrait and name plate. Replacing
the visible Japanese text while retaining only a guessed byte prefix produces an
incorrect speaker and corrupts the first visible English glyph.

`lil_sc2_opening_repair.nds` and `lil_sc2_opening_repair_v2.nds` are revoked
research candidates and must not be distributed. The safe integration baseline
is `out/raphael_natural_v2_accepted_base.nds`.

The replacement `out/lil_b22_first_screen_probe_v1.nds` changes only
`DK4_MES_B22_R0019`, Lil's first visible Amsterdam line. It preserves the `02`
selector, the record's exact 85-byte allocation, guarded line breaks, and ASCII
pair phase. The integrated builder admits block 22 only through this named,
research-only profile; every broader block-22 batch remains rejected. Cold-boot
confirmation of Lil's portrait/nameplate, first glyph, three-line rendering, and
transition to the following Kamil line is still required before expanding the
probe.

The expanded `out/lil_b22_intro_natural_v2_candidate.nds` now translates all
49 spoken records through Lil's order to sail for Bruges. It preserves every
inter-record scene command byte-for-byte and changes only the intended B22
dialogue records. Selector correlation is `02` = Lil, `09` = Kamil, `0E` =
Emilio, and `14` = Fernando; `FI` uses the three-byte default name `Lil`.
Because the first-screen result has not yet been reported from a cold boot, this
full build remains an experimental candidate rather than an accepted layer.

## Lil Deck tutorial manuscript

Lil's complete SC2 block-23 Deck-post tutorial now has a 35-record source-first
natural-English manuscript in
`translations/lil_natural_v2_sc2_b23_blocked.json`. It follows the actual route
sequence from Kamil's opening explanation through the prompt to open Deck and
change navigator assignments. Terminology matches the accepted interface,
including captain, sail master, helmsman, surveyor, lookout, Observation, Auto
Move, Half/Full sails, and the X Button.

Static correlation has now mapped selectors `02` = Lil, `09` = Kamil, `14` =
Fernando, and `FE` = the system tutorial panel. Records 18 and 20 are not
continuations: they are the two bare labels inside a choice command sequence
matching the proven Raphael tutorial grammar. `FI` is the default-route first-name
macro and therefore expands to `Lil`; `FA` and `FO` map to `Argot` and `Argot Co.`.
The evidence and record-by-record command map are in
`docs/lil_sc2_b23_control_map.md`.

This remains editorial progress rather than a release batch because the native
emulator window is unavailable to the current automation surface. Portrait and
nameplate presentation, choice placement, macro expansion, and final wrapping
still need a manual cold-boot pass. Every source record has an exact hex guard,
every English line remains in `blocked_records`, and the only buildable form is
the explicitly experimental seven-record control probe.

## Naming keyboard page selection

The naming popup still opens on the Japanese kana page. The visible `英` and `記`
entries are not ordinary captions: the keyboard manager also uses their exact encoded
values to identify the Latin and symbol pages. Replacing either value makes the
corresponding page render as a blank black panel.

For stability, the current build keeps those two functional identifiers unchanged.
The editor headings use direct translations such as `Name: Edit`; they no longer
contain instructions to press `英`.

Making Latin input the default remains a code-level task. It requires locating and
changing the keyboard manager's initial page index without modifying its page
identifiers. Until then, select `英` to reach the built-in Latin keyboard.

## Town-screen date suffixes

The compact date panel on town screens still renders Japanese `月` and `日` suffixes,
for example `1月 2日`. This is distinct from the translated birthday, inn-duration,
arrival-month, and shared calendar strings. It is also absent from the town graphics
atlas, indicating that the town HUD builds the date through a separate low-level
renderer.

Do not replace the shared Japanese font glyphs as a workaround: those glyphs remain
necessary for untranslated material and a global replacement would corrupt unrelated
screens. The safe follow-up is to locate the town HUD's formatter or glyph-emission
routine and change only that call site.

## Experimental lowercase descender adjustment

The embedded 6-by-11 ASCII glyphs for `g`, `j`, `p`, `q`, and `y` place ink on their
final bitmap row, which makes their tails look clipped when the DS image is enlarged.
The experiment that moved those five glyphs up one pixel did not improve the clipped
tails in the user's cold-boot test. The batch and release profile have been removed;
do not restore them or use `natural_dialogue_font_v4.nds` as a parent. This indicates
that the clipping occurs in the dialogue renderer's baseline/clip rectangle or in the
scaled presentation, not solely in the stored glyph bitmap.

The bare-newline candidate `out/dialogue_clean_lines_v1.nds` is revoked. Cold-boot
screenshots show the first glyph after `0A` appearing on the preceding line, producing
splits such as `man o/f`, `n/ow`, `B/ehold`, and `when w/e`. Static tracing had identified
a layout/parser routine but did not establish the progressive renderer's display timing.
Raphael builds now require `raphael-story-live`, protected `0A 20` breaks, and route-aware
macro widths. The one-cell guard indent remains preferable to lost or joined letters.

The protected space is visibly rendered, so continuation lines remain indented by one
cell. The disposable `0A 05` speaker-control experiment preserved the text and speaker
state but produced the same indent in all three cold-boot screenshots. It is rejected;
`out/dialogue_zero_indent_speaker_guard_probe.nds` must not be used as a parent.

Static tracing then identified the narrow path at `0x0207CFD0`: unlike the Shift-JIS
branch, it groups two single-byte characters into one draw call and advances both the
source and column counters by two. The disposable
`out/dialogue_ascii_single_byte_renderer_probe.nds` changes that path to terminate the
draw buffer after one byte and advance both counters by one. Cold-boot testing rejected
this hypothesis: `Ah, now` displayed as `Ah.n` followed by `ow`, and `Behold` displayed
as `B` followed by `ehold`. The continuation indent also remained. Therefore
`0x0207CFD0` is not the live progressive-story path for these records, and
`out/dialogue_ascii_single_byte_renderer_probe.nds` is revoked and must never be used
as a parent. No further bare-`0A` ROM may be handed off until the active call site is
proved with a runtime trace or breakpoint in the emulator.

Translators must never add leading spaces or artificial wording to influence layout.
`natural-dialogue-v2` and `scripts/audit_dialogue_batch.py` own ordinary wrapping and
block inherited manual breaks unless reviewed as a deliberate dramatic pause.

Fixed-size `{PAD}` bytes are also visible-width spaces. Excess padding after a full
page can create a blank dialogue box. `dialogue-fixed-v1` now rejects any record whose
padding would cross the four-line page boundary; do not disable that check to force a
build through.

## Route-specific leading dialogue state

Raphael SC0 block 48 uses printable leading state bytes `0x4B` for Hans Retzel and
`0x71` for the dock worker. Static sequence evidence and the legacy fixed-size batch
both preserve these values. They are mapped only in `raphael-story-live`; do not make
printable leading bytes global speaker controls. Leading `0x97`, `0xFE`, and other
unmapped states remain quarantined.

`out/raphael_full_natural_v2_candidate.nds` is revoked. Cold-boot testing exposed
blank skipped rows when a formatted first line occupied exactly 216 pixels: the
pair-phase protection byte triggered the native auto-wrap, then the stored newline
advanced a second time. The route-wide audit found 19 affected records.

`dialogue-fixed-v1` now rejects this shape as `pair-phase-auto-wrap`. The replacement
`out/raphael_full_natural_v2_skipfix_candidate.nds` rewrote every affected record. It
was later superseded by the parity-opening build that the user accepted as
`out/raphael_natural_v2_accepted_base.nds`.

## Revoked SC0 block-44 relocation proof

`out/raphael_b44_long_dialogue_relocation_poc.nds` is revoked. It rebuilt SC0 block 44
and expanded segments 13, 17, 21, 25, and 29 by a net 68 aligned bytes. Static checks
proved that every other ILNK block and NUL-delimited segment was unchanged, later ILNK
offsets moved by exactly 68 bytes, and protected ARM9 data was untouched. Those checks
were nevertheless incomplete: cold-boot testing rendered the first expanded box, then
advanced directly to town instead of the next dialogue.

This proves that block 44 has unresolved compiled-VM layout rules. A read-only failure
trace showed the VM reach the correct new end of the expanded first string and then
stop, disproving the initial simple stale-pointer explanation. NUL boundaries are
text-extraction conveniences, not a complete model of compiled-script control flow.
`translations/sc0_b44_relocation_map.json` is marked
incomplete and the builder now hard-fails this profile. The generated ROM and manifest
were moved from `out/` to `work/revoked/` with `.REVOKED` in their filenames. Do not
use, distribute, or base work on that ROM. Future expansion requires a decoded CS instruction stream and
rewriting every affected internal target, or a substitution design that leaves the
compiled block byte layout unchanged.

The follow-up `out/raphael_b44_long_dialogue_parity_poc.nds` established the missing
invariant: each replacement must retain the original record's odd/even byte phase. The
builder rejects an undeclared parity change and adds one manifest-recorded structural
trailing space when the relocation map explicitly permits it. Its five-box result was
subsequently incorporated into the accepted baseline.

The first parity probe intentionally contained only five story records, so subsequent
dialogue fell back to the former canonical ROM's mixture of Japanese and older English.
The hybrid `out/raphael_full_natural_v2_parity_opening_candidate.nds` added the reviewed
route batches and fixed the post-newline strings that lost their initial `J`, `W`, and
`L`. The user cold-boot tested and accepted that exact ROM; its bytes are preserved as
`out/raphael_natural_v2_accepted_base.nds`. Quarantined records with unmapped control
preambles remain outside the build and may still appear in Japanese later.

## Accepted full Lisbon-intro relocation

`out/raphael_intro_lisbon_natural_relocation_candidate.nds`, SHA-256
`3f5a447d5b5e12899eae178c74ef2694f1f62d5f77a7ffb1d15849ac3af9e278`, is
revoked. Cold-boot testing found three defects:

- the possessive suffix after the `FI` macro wrapped onto its own line;
- the shared crew-recruitment notice lost the initial `J` in `joined`; and
- expanding choice segments 454 and 456 from their original 8 and 14 bytes to
  22 and 20 bytes corrupted the second option and displaced the guided-tutorial
  branch entry, producing two blank prompts before town.

The choice failure proves those two option slots have fixed interior references.
Parity preservation alone is insufficient for them. They are now forbidden from the
relocation map and handled by an exact-allocation batch. The replacement profile also
removes the stored newline from shared crew record `DK4_MES_B04_R0059`, preserving
both `%s` offsets and the exact 43-byte allocation so automatic wrapping cannot drop
the first glyph after a protected break.

The replacement was completed as
`out/raphael_intro_lisbon_choicefix_centered_candidate.nds`, SHA-256
`fb750eac00d3c91cf0cc00e5ee578ba8d2d6eebd7791338c61003d003e5b09d3`.
Its exact 8-byte and 14-byte options are `Ask him.` and `Prepare alone.`; neither uses
invisible alignment padding. The user explicitly accepted and promoted this build on
2026-08-20. Its bytes are now the canonical baseline. Do not use the revoked
predecessor as a parent or release.

## Experimental Lisbon Trader tutorial completion

`out/raphael_tutorial_trader_complete_candidate.nds`, SHA-256
`4c2c1ccc034b0b2c1955a81c157f08b585bc8ee9e602dbd625867a8aeac00af5`, is an
experimental continuation of the accepted Lisbon baseline. It changes only
`/COMMON/MESFILE.DK4` and `/__arm9__.bin`.

The shared Trader archive contains eight records with multiple fixed interior entry
points. Their original offsets are executable layout facts: translating one packed
message as ordinary prose can overwrite an alternate prompt. The
`raphael-tutorial-trader` profile therefore uses exact-width raw replacements for
those records and tests every interior offset. Thirteen ordinary prompts use the
pair-phase-aware shared dialogue profile so automatic English wrapping cannot drop
the first continuation glyph.

The profile also contains 19 source-reviewed tavern and sailor-recruitment records:
hostess greetings and prices, insufficient-funds prompts, all seven independently
addressed recruitment voice variants, and the independently addressable shortfall
and spare-berth follow-ups. Six additional tavern/recruitment records contain two
or more concatenated messages with unproven interior entry offsets; they are listed
in `blocked_packed_records`, have complete editorial drafts, and deliberately remain
unchanged until their entry offsets are proven.

The market-report fee bubble originally stored `%s\n Fee: %s coins`. The accepted
progressive renderer can lose the first glyph after that stored newline, which
displayed `ee: 0 coins`. The experimental ARM9 batch keeps both `%s` substitutions
in order but renders the caption on one line as `%s: %s coins`.

Do not promote this candidate until a cold boot completes the guided Lisbon lesson,
exercises Trader and sailor-recruitment choices where practical, and verifies that
the market-report map displays its city and fee without missing characters.

# Release baseline warning

- `out/raphael_natural_v2_accepted_base.nds` is the user-designated safe integration
  baseline as of 2026-08-20.
- Its SHA-256 is `fb750eac00d3c91cf0cc00e5ee578ba8d2d6eebd7791338c61003d003e5b09d3`.
- `out/raphael_natural_v2_pre_lisbon_accepted_rollback.nds`, SHA-256
  `fe7cdcaf7cfa24f18c1c48608ddddf58dc9a7555cb93c8131163037e814c8586`,
  is the immediate immutable rollback artifact; it is no longer the parent for new
  playable work.
- All later integration, route, repair, and probe ROMs—including `lil_route_roundtrip.nds`, `raphael_complete_en.nds`, `raphael_complete_fixed.nds`, and the Lil repair probes—are deprecated historical artifacts. Do not distribute them or use them as a base.
- Run `scripts/verify_release_baseline.py out/raphael_natural_v2_accepted_base.nds <candidate.nds>` before handing off any subsequent candidate.

## Misclassified SC2 Lil-route block-27 manuscript

`translations/hodram_natural_v2_sc2_b27_blocked.json` replaces the old literal,
manually wrapped draft with 49 source-first natural-English records. Despite the
historical filename, this is a Lil-route scene, not Hodram's playable opening. It covers
Lil and Kamil's harbor encounter with Hodram and Gerhard, including
the confrontation, Kamil's private apology, and Hodram's reassurance.

This is deliberately not a build batch. SC2 block 27 uses leading states `0x01`,
`0x02`, `0x09`, `0x10`, and `0x14`, and its `FI` expansion refers to Lil inside
Lil's route. Their portrait/name effects and runtime expansion behavior have not
been independently mapped. The manuscript records the exact source prefix and source
length for every line, preserves every `FI` occurrence as `{MACRO:FI}`, and leaves
the formatting review gate false. Do not revive the guessed `{HEX:...}` controls or
manual `{LB}` layout from `translations/hodram_route.json`.

## Misclassified SC2 Lil-route block-66 manuscript

`translations/hodram_natural_v2_sc2_b66_blocked.json` contains a complete
72-record source-first natural-English draft of the Kamil/Antony Kuhn reunion and
family-history sequence. Together with block 27, the Lil-route manuscript now
covers 121 records without reusing the legacy batch's mojibake, manual `{LB}`
wrapping, or guessed `{HEX:...}` controls.

This remains editorial-only. The exact leading bytes `01`, `02`, `09`, `0E`,
`14`, and `28` are source-locked, and every `FI` occurrence is preserved as a
macro placeholder. The leading `0x28` on Antony's lines may be a literal thought
marker rather than a presentation state, so it must not be promoted to a control
token without runtime evidence. Lil-route portrait/name behavior and the
cross-route `FI` expansion must be mapped before formatting or insertion.

## Misclassified SC2 Lil-route block-146 manuscript

`translations/hodram_natural_v2_sc2_b146_blocked.json` adds all 35 records from
the scene where Kamil leaves Lil, meets Hodram, and accepts a temporary berth on
his ship. The historical Hodram-named files cover all 156 Lil-route records identified
in the legacy three-block batch: 49 in block 27, 72 in block 66, and 35 in
block 146.

Block 146 is not buildable yet. It mixes known-looking `01/02/09/14` leads with
bare Kamil records, an unexplained `0x97` lead, an `0xFE` narration lead, and the
cross-route `FI` macro. The draft records these facts explicitly and does not
convert them into guessed control tokens. Runtime state mapping and formatter
evidence are required before any record can move into a release batch.

## Revoked wrong-route SC2 control-map probe

`out/hodram_sc2_control_map_probe_v1.nds` is a research-only integrated probe,
SHA-256 `e77b5668d18d320913510e783c08d8098f9437042267876a4998750d4896d9fe`.
It was built from the accepted Raphael baseline through profile
`hodram-sc2-control-map-probe`. Only six exact-allocation records in
`/data/SC2.DK4` block 27 change. Each original lead byte is retained verbatim;
no record offset, length, newline, or other ROM file changes.

The user confirmed that the ROM loads, but the scene is not reachable by following
Hodram's New Game path: SC2 block 27 belongs to Lil's route. The profile is revoked.
Do not test, distribute, promote, or use this ROM as a parent.

## Hodram SC1 opening English probe awaiting cold-boot test

`out/hodram_intro_english_probe_v1.nds`, SHA-256
`59af70e76736793cc4f1051ce8320e95f570159ef175df0d9a627fd323f17deb`,
is the corrected experimental candidate. It changes only `/data/SC1.DK4` and contains
67 QA-clean fixed-allocation records across blocks 42-44: the opening fleet exercise,
Hodram's speech, strategic trade tutorial, initial objective, and first Lil/Kamil
encounter. SC1's four-byte non-prose B42 R0032 fragment remains byte-identical.

The candidate uses the accepted guarded pair-phase renderer behavior and preserves
all source presentation states. The SC1 state effects and Hodram `FI`/`FA` macro
lengths are not yet runtime-proven, so this ROM is experimental and must not become a
parent. Cold-boot New Game as Hodram and verify every portrait/nameplate, wrapping,
the `FA` address in the post-speech exchange, the `FI` address after Lil leaves, and
normal progression through the first objective and Lil/Kamil encounter.

## Experimental Hodram Stockholm and tavern repair candidate

`out/hodram_stockholm_tavern_complete_candidate_v1.nds`, SHA-256
`fb8600a7cd8318493b91c7eb9511c1dc36ad03622ad72044aad13ac6408673d5`, is an
experimental continuation of the accepted Raphael baseline through profile
`hodram-stockholm-tavern-complete`. It changes only `/data/SC1.DK4`,
`/COMMON/MESFILE.DK4`, and `/__arm9__.bin`.

The candidate retains the 67-record Hodram opening and adds every mapped Japanese
dialogue record in the first Stockholm tavern, dock, and market tutorials (SC1
blocks 134-136). It also fills Gerhard's previously omitted surname slot with
`Ardelknatts`. The original audit covered only 8-, 12-, and 16-byte name records and
therefore missed Kamil's twenty-byte `Overijssel` slot. The complete profiled shared
name catalogue now contains 190 records; the Lil shared-data V2 candidate verifies
that all 190 resolve to terminated ASCII.

The shared tavern repair preserves each proven packed interior entry point while
fixing the reported bare price, lowercase diagnostic, empty Francisca response,
broken Clifford introduction, and terse rumor/strength lines. All new fixed-dialogue
records pass the natural-dialogue audit with no warnings or errors; packed records
have exact-offset regression tests.

Do not promote this ROM until a cold boot completes Hodram's opening and visits all
three first-Stockholm buildings. Test both tutorial choices, tavern purchases,
Francisca, sailor recruitment, nameplates, menus, wrapping, and every return to town.

## Lil intro shared-data V2 candidate awaiting cold-boot test

`out/lil_b22_intro_shared_data_v2_candidate.nds`, SHA-256
`b6c51e7c0211ba65df37385f90f177d65dbd37974734282a494fc845c8022346`, layers
the complete 49-record Lil Amsterdam intro on the canonical accepted baseline. It
also translates Kamil's shared surname to `Overijssel`, redirects all four shared
fleet-name formatters to a terminated `%s Fleet` string, translates Bruges' region
to `Flanders`, redirects its single-slot hemp label to terminated `Hemp`, and changes
the market-information location prompt to `Target`.

The shared crew-join formatter now keeps its byte-20 runtime entry point but begins
that second string with an ordinary sacrificial space. This establishes ASCII pair
phase before the `%s` name expansion and prevents the first character of names such
as `Fernando` from being consumed. The candidate changes only `/data/SC2.DK4`,
`/__arm9__.bin`, and `/COMMON/MESFILE.DK4`; baseline and sound-selector verification
pass, as do all 295 automated tests. It remains experimental until Kamil's nameplate,
Lil Fleet, the Fernando recruitment notice, and the full Bruges port-information
panel are reviewed from a cold boot.

The current successor is `out/lil_b22_intro_guild_inn_v4_candidate.nds`, SHA-256
`b12429f896e7d765c6979c0a1efa1d6648ccacaa83cb977ee1dc6e634f22105b`. It retains
all V2 repairs and adds every shared Innkeeper and Guildmaster nameplate, Buy/Sell
Items, the Ancient Map pitch, Gift/Price labels, and all three items offered by the
Amsterdam Guild: `Rainbow Marbles`, `Huizong Art`, and `Snow-Silk Robe`. All three
descriptions are English. The two packed description records preserve their neighboring
items and every internal entry offset. Baseline and sound-selector verification pass,
as do all 301 automated tests. Cold-boot review of all three selectable item panels is
still required before promotion.

# Revoked protected-newline probe (2026-08-14)

`out/dialogue_protected_newline_probe.nds` is revoked and must not be tested,
distributed, or used as a parent. Its helper overwrites live structured data at
`0x02172300`. `dialogue_live_safe_v3.nds` remains the safe dialogue baseline,
and protected `0A 20` breaks remain mandatory in translation data.

## Shipyard-complete V1 candidate awaiting cold-boot review

`out/shipyard_complete_v1_candidate.nds`, SHA-256
`c9371c510dbc3c70c2aea6cc13bf5b4d752e65da2ce6c5708b687444a70163ad`,
extends the complete placeholder-English candidate through the reported Shipyard
flows. It localizes Repair, Remodel, equipment-room headings and descriptions,
Reset and Back confirmations, Rename, dock status, ship-swap empty slots, purchase
confirmation, and the complete six-name cannon table.

The packed remodel and rename messages retain their original interior entry starts.
Every ASCII entry begins with a two-byte guard, every explicit continuation is
guarded, and every line is at most 31 bytes. The Repair record now uses the same
two-byte guard for both its primary response and byte-26 helper response, fixing
the dropped `N` in `No ships need repairs!`.

The existing 119-entry ship-model catalog was re-audited and remains unchanged.
`Fluyt` and `Pinnace` are the correct historical English terms; `Sm Galley` and
`Lg Galley` are deliberate compact forms required by the fixed list slots. The
accepted Ships-screen plaque geometry and runtime stat formatters also remain
unchanged. All 326 automated tests pass, but the candidate is experimental until
the complete Shipyard flow is reviewed from a cold boot.

## Experimental Lil Sphinx V26 candidate

`out/lil_deep_route_v26_candidate.nds`, SHA-256
`985824b0935da6baf51925dc522a993ccd8505665fb6fc8ee07bbf25925ee4f1`,
extends Lil V25 with all 36 source-reviewed B105 Sphinx-riddle records. It was built
through `lil-deep-route-v26` on the accepted integrated base (SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`).
The exact 36 B105 and preceding 42 V25 encoded records were found in the saved
candidate. The exhaustive V26 text audit has zero blockers, all integrated manifest
checks passed, eight targeted Lil tests passed, and the baseline invariant check
passed for the five declared internal paths.

The `CF` party-reaction byte has source-identical cross-route evidence; `82`, `8E`,
and `92` begin ordinary Japanese choice text. Static checks retain the `CF` state,
retain the first English glyph of each choice, and use guarded, pair-phase-safe
wrapping. The Sphinx's presentation,
choice branches, first glyphs, and scene transition still need cold-boot review.
This candidate remains experimental and is not the canonical parent.

## Experimental Lil cult and lamp V27 candidate

`out/lil_deep_route_v27_candidate.nds`, SHA-256
`24e3499c164978a09e52646c89079c2b136493cbbd8ea632480a03afc68a5570`,
extends Lil V26 with all 45 B106 cult-confrontation records and all 10 B108
hidden-believer lamp records. It uses the accepted integrated base (SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`)
and the registered `lil-deep-route-v27` profile. The exhaustive 55-record text
audit has zero blockers. Ten targeted Lil tests, all integrated manifest checks,
the baseline invariant check, and exact-byte checks of the 55 V27 and 36 V26
records in the saved candidate passed.

`B1` and `B2` mark the cult leader and cultists, supported by source-identical
SC0/SC1 lines. `A0` marks the village speaker in B106 and the hidden believer
in source-identical B108 lines. B106 records beginning `89 BD` begin the ordinary
Japanese glyph 何; their English starts with its first character and has no
speaker selector. Portraits, nameplates, first glyphs, and transitions await
cold-boot review. V27 remains experimental and must not replace the canonical
base without explicit user acceptance.

## Experimental Lil temple-clue V28 candidate

`out/lil_deep_route_v28_candidate.nds`, SHA-256
`0ad8a8bb27792eef81157720039fec8fe60361b5bbdb451653fe0479bd21b242`,
extends Lil V27 with the 16 spoken B107 temple-clue records. It was built from
the accepted integrated base (SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`)
through the registered `lil-deep-route-v28` profile. The 16-record dialogue
audit has zero blockers, 12 targeted Lil tests pass, every manifest check passes,
and the baseline invariant check passes. Exact-byte inspection of the saved ROM
finds all 16 V28 and 55 V27 records.

B107 R0003 is an unmapped four-byte fragment, `10 46 94 80`, rather than a
coherent spoken sentence. V28 explicitly excludes it, and exact-byte inspection
confirms the candidate leaves it unchanged. The scene's temple voice, clue
repetition, first glyphs, and transition need cold-boot review. V28 remains
experimental and must not replace the canonical base without user acceptance.

## Experimental Lil Colosseum V29 candidate

`out/lil_deep_route_v29_candidate.nds`, SHA-256
`d91f33cac03cac6f4a25584ea6eeb53c2f798c0014fa37a4e8c8d66ff36ed94b`,
extends Lil V28 with 55 B109 doubling-bean riddle records and 18 B110 urn-puzzle
records. It was built through registered profile `lil-deep-route-v29` from the
accepted base `out/raphael_natural_v2_accepted_base.nds` (SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`).
All 73 new records have zero blocking dialogue-audit issues and were visually
reviewed in ten preview sheets. Fourteen targeted Lil tests and Ruff pass. The
manifest's thirteen checks, accepted-base invariant, and exact-byte inspection
of all 73 new and 16 V28 records pass. The candidate changes only
`/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
`/_pxl/personinfo.pxl`, and `/data/SC2.DK4` from the accepted base.

B109 R0281 is an unmapped six-byte fragment, `96 47 21 48 51 A8`. It is explicitly
excluded and verified unchanged. The six mapped presentation states, ordinary
Shift-JIS text starts, and Lil's `FI` name macro are documented in
`docs/lil_sc2_b109_b110_control_note.md`. The riddle's three answers, urn choices,
portrait behavior, first glyphs, and transitions still need cold-boot review.
V29 remains experimental and must not replace the canonical base without user
acceptance.

## Experimental Lil gold-temple V30 candidate

`out/lil_deep_route_v30_candidate.nds`, SHA-256
`223970c3aa01d0940582d7904a24a6409963d6610edcb04bc5c0ea9928b46002`,
extends V29 with 33 B111 monk-scene spoken records. It was built through the
registered `lil-deep-route-v30` profile from the accepted base
`out/raphael_natural_v2_accepted_base.nds` (SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`).
All 33 dialogue records have zero blocking audit issues and were visually
reviewed in five preview sheets. Sixteen Lil regression tests and targeted
Ruff pass. The manifest's thirteen checks, accepted-base invariant, and
exact-byte inspection of all 33 V30 and 73 V29 records pass. Only
`/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
`/_pxl/personinfo.pxl`, and `/data/SC2.DK4` differ from the accepted base.

B111 R0062 and R0138 are identical three-byte monk-state ellipses,
`89 81 63`. They remain unchanged as explicit exclusions. The B111 monk's
leading `89` is a presentation state, while B109 `89` starts ordinary text;
the per-batch profile mapping is documented in
`docs/lil_sc2_b111_control_note.md`. The monk's portrait, nameplate, first
glyphs, and transition need cold-boot review. V30 remains experimental and
must not replace the canonical base without user acceptance.

## Experimental Lil sandbar-rescue V31 candidate

`out/lil_deep_route_v31_candidate.nds`, SHA-256
`dee2ae42f9d262671326a85b1d8f71405bdf01033f2c203a7f5c6e0cc9001a25`,
extends V30 with all 30 B112 spoken rescue records. It was built through the
registered `lil-deep-route-v31` profile from the accepted base
`out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
The dialogue audit has zero blockers; all 30 previews were reviewed. Eighteen
targeted Lil tests and Ruff pass, as do all thirteen manifest checks, the
accepted-base invariant, and saved-ROM exact-byte checks for the 30 V31 and
33 V30 records. Only `/COMMON/MESFILE.DK4`, `/__arm9__.bin`,
`/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`, and `/data/SC2.DK4` differ
from the accepted base.

B112 R0010 is the seven-byte non-prose fragment `46 8F 80 80 43 1E 63` and is
verified unchanged. The child, grandfather, lookout, rescuer states and ordinary
`81/82/8E/94` text starts are documented in `docs/lil_sc2_b112_control_note.md`.
The rescue, gift event, short companion variants, portraits, first glyphs, and
scene transition still need a cold-boot sample. V31 remains experimental and
must not replace the canonical base without explicit user acceptance.

## Experimental Lil jade-and-cacao V32 candidate

`out/lil_deep_route_v32_candidate.nds`, SHA-256
`f8cb242cb0d5038b4a4e8a8fd016f06e2e1da540764fd0314b46002a2fa74449`,
extends V31 with six B113 jade-discovery and thirteen B114 cacao-follow-up
records. The registered `lil-deep-route-v32` profile builds from accepted base
`out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
The 19-record audit has zero blockers, and every preview was reviewed. Twenty
targeted Lil tests and Ruff pass, all thirteen manifest checks pass, and the
accepted-base invariant and saved-ROM checks find the exact 19 V32 and 30 V31
records. Only `/COMMON/MESFILE.DK4`, `/__arm9__.bin`,
`/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`, and `/data/SC2.DK4` differ
from the accepted base.

B113 R0004 (`60 30 46 93 80 3E 63`) and R0025 (`30 48 8B A8`) are verified
unchanged. The townsman's printable `68` state and ordinary companion text
starts are documented in `docs/lil_sc2_b113_b114_control_note.md`. The jade
event, scholar portrait, cacao branch, town nameplate, first glyphs, gate unlock,
and transitions still need a cold-boot sample. V32 remains experimental and
must not replace the canonical base without user acceptance.

## Experimental Lil tablet-and-recruitment V33 candidate

`out/lil_deep_route_v33_candidate.nds`, SHA-256
`c11b4df0f5b35de8f445d9a440b313e525760fd3efa7a957b7f8bd02659e15ff`,
extends V32 with all 37 B115 records. The registered `lil-deep-route-v33`
profile builds from `out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
All 114 accepted layers are baked into that base; the cumulative profile adds
43 experimental batches. The audit has zero blockers, all 37 previews were
reviewed, 22 targeted Lil tests and Ruff pass, and all 13 manifest checks pass.
Saved-ROM checks verify 37 V33 and 19 V32 exact records and two unchanged B113
exclusions. The baseline invariant passes with only the declared cumulative
paths `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
`/_pxl/personinfo.pxl`, and `/data/SC2.DK4` changed.

B115 includes a shared Maria branch: source-correlated `03` is Maria, not Lil;
`04` is Janus and `B4` is the raider. R0089 starts with staging LF, not speaker
state `0A`; English starts directly with `B`. R0078 preserves FO. See
`docs/lil_sc2_b115_control_note.md` and `docs/lil_v33_checkpoint.md`.
Runtime portraits, macro expansion, first/continuation glyphs, recruitment,
reward and transitions still need cold-boot review. V33 remains experimental.
Coverage is 2,492/6,608 translated, 4,092 remaining and 24 excluded.

## Experimental Lil India-tip, figurehead, and tribal-reward V34 candidate

`out/lil_deep_route_v34_candidate.nds`, SHA-256
`a84f93aa47163fb7fc3840c7b23ef5007c0f76f2a11253be744e6976b0f33680`,
extends V33 with 30 B116-B118 records. Registered profile `lil-deep-route-v34`
builds from `out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
All 114 accepted layers are baked into the base; 44 experimental batches apply.
Zero audit blockers remain, every preview was reviewed, 24 Lil regression tests
and Ruff pass, all 13 manifest checks pass, and the baseline invariant passes.
Saved-ROM checks verify 30 exact V34 and 37 exact V33 records plus both new
unchanged exclusions. Only `/COMMON/MESFILE.DK4`, `/__arm9__.bin`,
`/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`, and `/data/SC2.DK4` change.

C6/D1/DC/B3 are source-correlated presentation states; 82/91 start ordinary
text. B117 R0004 `60344693803F63344872A8` and B118 R0004 `60944695803B63`
remain non-prose exclusions. The India tip uses the subcontinent to avoid the
unsafe literal uppercase I byte while preserving the location reference.
See `docs/lil_sc2_b116_b118_control_note.md` and `docs/lil_v34_checkpoint.md`.
Gift trigger, map gate, figurehead acquisition, knife ownership, 24,000-gold
reward, portraits, first/continuation letters and transitions require cold-boot
review. V34 remains experimental. Coverage: 2,522/6,608 translated; 4,060
remaining; 26 excluded. Continue at B120, then B121.

## Experimental Lil sailing-tutorial V35 candidate

`out/lil_deep_route_v35_candidate.nds`, SHA-256
`6ca22311b6f1f02d49431ceebe8cfa1fd9cd8cf33eb04dcf0104ae3f1f41971a`,
completes B120 with 28 new records plus V21's inherited refusal. Registered
profile `lil-deep-route-v35` builds from the accepted base
`out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
All 114 accepted layers are baked into that base; 45 experimental batches apply.
The audit has zero blockers, all previews were reviewed, 26 targeted tests and
Ruff pass, and all 13 manifest checks pass. Exact saved-ROM checks cover all
29 cumulative B120 records and 30 V34 records with both exclusions unchanged.
The baseline invariant passes; only `/COMMON/MESFILE.DK4`, `/__arm9__.bin`,
`/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`, and `/data/SC2.DK4` change.

Both FI macros and 02/09/FE states are preserved; 82/95 begin ordinary text.
See `docs/lil_sc2_b120_control_note.md` and `docs/lil_v35_checkpoint.md`.
Cold-boot all tutorial answers, controls, portraits, macro expansion, first
letters and arrival before acceptance. V35 remains experimental.
Coverage is 2,550/6,608 translated, 4,032 remaining and 26 excluded.

## Experimental Lil ambush and reconciliation V36 candidate

`out/lil_deep_route_v36_candidate.nds`, SHA-256
`718745efda5341c3253512a94f5bb00bdc560b0b6a6cb57c948b0abe7807cb17`,
completes all 109 B121 records. Registered profile `lil-deep-route-v36` builds
from `out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
All 114 accepted layers are baked into that base; 46 experimental batches apply.
The dialogue audit has zero blockers, all previews were reviewed, 28 targeted
tests and Ruff pass, and all 13 manifest checks pass. Saved-ROM checks verify
109 V36 records, 28 V35 records and the V21 tutorial refusal exactly. The baseline
invariant passes with only the five declared cumulative paths:
`/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
`/_pxl/personinfo.pxl`, `/data/SC2.DK4`.

No new control mapping is introduced. Fourteen presentation states and ten FI
macros are preserved; 8C/91 choices begin directly with E/R. See
`docs/lil_sc2_b121_control_note.md` and `docs/lil_v36_checkpoint.md`.
Cold-boot both combat choices and rescue branches, Kamil's return, the farewell
and Proof-map reward. Runtime portraits, nameplates, macros, first/continuation
letters and transitions require review. V36 remains experimental.
Coverage: 2,659/6,608 translated; 3,923 remaining; 26 excluded. Continue at B122.

## Paused Lil goal and combined four-route candidate

At the user's request, Lil is paused and the current work is compiled into
`out/all_routes_unified_lil_v37_candidate.nds`, SHA-256
`b5eecc91403fbdef91e955f04a8ec0251863c0ba701f6960ae19401c5b86757f`.
Registered `all-routes-unified-v3` retains the 290-batch unified V2 stack
(Raphael V93, Hodram V32, Maria V111 and shared repairs) and adds Lil V24–V37,
for 304 experimental batches. All 114 accepted layers remain baked into the
immutable base `out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.

The current B122 scene is finished with 30 records and three FI macros. All
previews were reviewed; zero audit blockers remain. Seven targeted tests and
Ruff pass, all 13 build checks pass, hashes are verified, and the baseline
invariant passes with exactly nine declared paths. Direct raw-block checks
verify all 18,399 experimental route records and 195 unchanged exclusions.
See `docs/all_routes_unified_lil_v37_checkpoint.md` for full identity,
changed paths, reports and cold-boot test areas.

This remains experimental; cold-boot acceptance and promotion are pending.
Lil coverage is 2,689/6,608 translated, 3,893 remaining and 26 excluded.
Resume at B123 only when requested. No additional scene work follows the pause.

## Resumed Lil B123–B124 and combined V4 candidate

The user resumed Lil translation with a natural-English requirement. All 22
B123–B124 records are translated and every preview is reviewed. Audit has zero
blockers. `out/all_routes_unified_lil_v38_candidate.nds`, SHA-256
`8fba208bdd8844b5d9baf2dc8e9dcb54607835b0a41cf3cc46d47010679f0285`,
uses `all-routes-unified-v4` (305 experimental batches) over the same immutable
accepted base, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
It carries Raphael V93, Hodram V32, Maria V111 and Lil V38 plus the shared
layers. All 114 accepted layers remain baked into the base. Thirty-five
targeted tests and Ruff pass; all 13 manifest checks, hashes and baseline
invariant pass. Exactly nine declared internal paths change. Direct saved-ROM
verification confirms 18,421 experimental route records and 195 unchanged
exclusions. See `docs/all_routes_unified_lil_v38_checkpoint.md` and
`docs/lil_sc2_b123_b124_control_note.md`.

Runtime review remains pending. Verify Christina's grandfather, Julian's
portrait and natural dialogue, the Snowfall Robe clue, opening/continuation
letters, and the earlier scenes in a cold boot. No baseline promotion.
Lil coverage: 2,711/6,608 translated, 3,871 remaining, 26 excluded.

## Experimental four-route Lil V40 candidate

After resuming translation, B125 (44 records) and B126 (15 records) were
localized into natural American English from clean Japanese. Their exhaustive
audits have zero blockers and all previews were visually reviewed. Both
choice paths, FI macros, the established Guiding Staff name, the spirit
reward, and the Bruges trading mechanics are retained. See
`docs/lil_sc2_b125_b126_control_note.md`.

`out/all_routes_unified_lil_v40_candidate.nds`, SHA-256
`66f38a04ccfdbdd1b1cef1fe47f798c40e61e71dcde5f600296ab326efcb1b47`,
uses `all-routes-unified-v6`, with 307 experimental batches over the immutable
base `out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
All 114 accepted layers remain baked into the base. Raphael V93, Hodram V32,
Maria V111 and Lil V40 are combined. Thirty-nine targeted tests and Ruff pass;
all 13 manifest checks, hashes and the baseline invariant pass with the nine
declared changed files. Saved-ROM checks verify 18,480 exact experimental
route records and 195 unchanged exclusions. See
`docs/all_routes_unified_lil_v40_checkpoint.md`.

This remains experimental; cold-boot testing is pending. Lil coverage is
2,770/6,608 translated, 3,812 remaining and 26 excluded. Continue B127.

## Experimental four-route Lil V44 candidate

The user asked to continue the goal through completion. B127–B132 add 145
source-reviewed natural-English Lil records. The exact-font previews for
every new line were reviewed for wraps and leading characters; exhaustive
audits have zero blockers. B131 R0080 is an opaque four-byte `23 48 9B A8`
event payload and remains unchanged as a new explicit exclusion. See
`docs/lil_sc2_b127_b132_control_note.md`.

`out/all_routes_unified_lil_v44_candidate.nds`, SHA-256
`3cc2be4c1a5788cb43bdebd5520d33fb767ab253ccd16b68af9808c3b4325c87`,
uses `all-routes-unified-v10` with 311 experimental batches over the
unchanged accepted base, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
The 114 accepted layers remain baked in. Forty-one targeted tests and
Ruff pass; all 13 build checks, hashes and the accepted-base invariant
pass with the nine registered changed paths. Saved-ROM verification finds
18,625 exact experimental route records and 196 byte-identical exclusions.
See `docs/all_routes_unified_lil_v44_checkpoint.md`.

Runtime cold-boot review and explicit acceptance remain pending. Lil
coverage is 2,915/6,608 translated, 3,666 remaining and 27 excluded.
Continue at B133, the Raphael Castor crossover.

## Experimental four-route Lil V47 candidate

B133–B136 add 109 source-reviewed natural-English Lil dialogue records.
Their exact-font preview sheets were visually checked, including individual
inspection of two B133 first glyphs that looked cropped on contact sheets.
B136 R0020 is an opaque four-byte `23 48 9D A8` event payload, excluded
unchanged. See `docs/lil_sc2_b133_b136_control_note.md`.

`out/all_routes_unified_lil_v47_candidate.nds`, SHA-256
`1be6b03e0c44e05a9b7bf193281b19e8c7f543df5cbca0cd3907a1b89c9b75aa`,
uses `all-routes-unified-v13` with 314 experimental batches over the
unchanged accepted base. All 13 build checks, 28 targeted tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
18,734 exact experimental route records and 197 unchanged exclusions.
See `docs/all_routes_unified_lil_v47_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
3,024/6,608 translated, 3,556 remaining and 28 excluded. Continue B137.

## Experimental four-route Lil V48 candidate

B137 adds 47 source-reviewed natural-English Lil dialogue records covering
Nagalpur's tavern confrontation. Exact-font preview sheets were reviewed,
including individual inspection of first glyphs that looked cropped on
contact sheets. See `docs/lil_sc2_b137_control_note.md`.

`out/all_routes_unified_lil_v48_candidate.nds`, SHA-256
`9b18a2142f1860d857b2cfb0d6f3b6aead4c1af4a91b25322c9ba6dbac85240a`,
uses `all-routes-unified-v14` with 315 experimental batches over the
unchanged accepted base. All 13 build checks, 29 targeted tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
18,781 exact experimental route records and 197 unchanged exclusions.
See `docs/all_routes_unified_lil_v48_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
3,071/6,608 translated, 3,509 remaining and 28 excluded. Continue B138.

## Experimental four-route Lil V50 candidate

B138–B139 add 55 source-reviewed natural-English Lil dialogue records
following the B137 Nagalpur confrontation. Their exact-font previews
were reviewed, including individual first-glyph inspection. B139 R0035
is an opaque four-byte `23 48 9E A8` event payload and remains unchanged.
See `docs/lil_sc2_b138_b139_control_note.md`.

`out/all_routes_unified_lil_v50_candidate.nds`, SHA-256
`bd4bc044969e5f0abb9bc60babd94a4c87e20628b4ed11e006f29955e4c014d4`,
uses `all-routes-unified-v16` with 317 experimental batches over the
unchanged accepted base. All 13 build checks, 30 targeted tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
18,836 exact experimental route records and 198 unchanged exclusions.
See `docs/all_routes_unified_lil_v50_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
3,126/6,608 translated, 3,453 remaining and 29 excluded. Continue B140.

## Experimental four-route Lil V54 candidate

B140–B145 add 101 source-reviewed natural-English Lil dialogue records:
the Lelystad polder pledge and funding branches, armor-upgrade research and
completion, and the Mediterranean Proof map reveal. Exact-font previews were
reviewed and ambiguous first glyphs checked individually. B145 R0021 is an
opaque four-byte `23 48 9C A8` reveal event, excluded unchanged. See
`docs/lil_sc2_b140_b145_control_note.md`.

`out/all_routes_unified_lil_v54_candidate.nds`, SHA-256
`d74e21082ad700d024f65aec14bb82db4a7c4b2053d46594313b6943c4b4d830`,
uses `all-routes-unified-v20` with 321 experimental batches over the
unchanged accepted base. All 13 build checks, 34 targeted tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
18,937 exact experimental route records and 199 unchanged exclusions.
See `docs/all_routes_unified_lil_v54_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
3,227/6,608 translated, 3,351 remaining and 30 excluded. Continue B146.

## Experimental four-route Lil V55 candidate

B146 adds 35 source-reviewed natural-English records covering Kamil's
separation from Lil and Hodram's sailing invitation. The `97` sailor voice,
`FE` narration and both `FI` macros retain their source control behavior.
All exact-font previews were reviewed. See `docs/lil_sc2_b146_control_note.md`.

`out/all_routes_unified_lil_v55_candidate.nds`, SHA-256
`cdec3ad9981f3586736ce5f8ae9d74e179bb95d99c4627f4863e46bd00699332`,
uses `all-routes-unified-v21` with 322 experimental batches over the
unchanged accepted base. All 13 build checks, 35 targeted tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
18,972 exact experimental route records and 199 unchanged exclusions.
See `docs/all_routes_unified_lil_v55_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
3,262/6,608 translated, 3,316 remaining and 30 excluded. Continue B147.

## Experimental four-route Lil V56 candidate

B147 adds 68 source-reviewed natural-English records: Maria's identity
reveal, warning that Kuhn is using Lil, the possible planted Li crest, and
the Batavia lead. Both companion departure variants are translated. The
`FI` and `FA` name macros, five guarded elder line-break openings, and the
R0021 first-glyph layout exception were previewed. R0129 is an opaque
four-byte `21 46 83 80` reveal event and remains unchanged. See
`docs/lil_sc2_b147_control_note.md`.

`out/all_routes_unified_lil_v56_candidate.nds`, SHA-256
`26a0db5ae7e1f42194d2e0893dcfa9dd78eb7854c49dada058ff992020736b2a`,
uses `all-routes-unified-v22` with 323 experimental batches over the
unchanged accepted base. All 13 build checks, 36 targeted tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
19,040 exact experimental route records and 200 unchanged exclusions.
See `docs/all_routes_unified_lil_v56_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
3,330/6,608 translated, 3,247 remaining and 31 excluded. Translation work
is paused at this completed set until the user resumes it; B148 is next.

## Experimental four-route Lil V57 candidate

B148-B149 add 45 source-reviewed natural-English records. A Batavia witness
reveals the name Kamil in Kuhn's family history; the Tang Bamboo Craft and
Bamboo Assembly Plan then reveal the East Asia Proof map across both Kamil
and Fernando branches. All exact-font previews were reviewed, and B149's
`FI` name macro retains its source behavior. See
`docs/lil_sc2_b148_b149_control_note.md`.

`out/all_routes_unified_lil_v57_candidate.nds`, SHA-256
`e31e356eed71036439b2d55eff70f5d0c75c51a93aed005d0b8a8712f3b4cf35`,
uses `all-routes-unified-v23` with 324 experimental batches over the
unchanged accepted base. All 13 build checks, 37 targeted tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
19,085 exact experimental route records and 200 unchanged exclusions.
See `docs/all_routes_unified_lil_v57_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
3,375/6,608 translated, 3,202 remaining and 31 excluded. Continue B150.

## Experimental four-route Lil V58 candidate

B150 adds 22 source-reviewed natural-English records. Clifford explains
Maldonado and Escante's alliance in the New World and asks Lil to strike
Maldonado while they build strength for Escante. The `FO` faction macro
retains its source behavior. All exact-font previews were reviewed. See
`docs/lil_sc2_b150_control_note.md`.

`out/all_routes_unified_lil_v58_candidate.nds`, SHA-256
`16ec7b5a8db384752421e85850f637281e469f1667a72da87ea7b79d5221325c`,
uses `all-routes-unified-v24` with 325 experimental batches over the
unchanged accepted base. All 13 build checks, 38 targeted tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
19,107 exact experimental route records and 200 unchanged exclusions.
See `docs/all_routes_unified_lil_v58_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
3,397/6,608 translated, 3,180 remaining and 31 excluded. Continue B151.

## Experimental four-route Lil V60 candidate

B151-B153 add 70 source-reviewed natural-English records. Maldonado's
tavern confrontation includes alternate monologues, companion reactions,
and aftermath branches. The Ancient Kingdom Coin and Lotion Jar reveal the
Southeast Asian Proof map; opaque B153 R0024 (`23 48 9F A8`) stays unchanged.
The `2A` Maldonado presentation state and all `FI`, `FA`, and `FO` macros
are preserved. All exact-font previews were reviewed. See
`docs/lil_sc2_b151_control_note.md` and
`docs/lil_sc2_b152_b153_control_note.md`.

`out/all_routes_unified_lil_v60_candidate.nds`, SHA-256
`68d881c5f938f637157f9fa16c8d85b212f17689d1d9c6f0602afb7cc01958b9`,
uses `all-routes-unified-v26` with 327 experimental batches over the
unchanged accepted base. All 13 build checks, 40 targeted tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
19,177 exact experimental route records and 201 unchanged exclusions.
See `docs/all_routes_unified_lil_v60_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
3,467/6,608 translated, 3,109 remaining and 32 excluded. Continue B154.

## Experimental four-route Lil V61 candidate

B154 adds 40 source-reviewed natural-English records for Al's dismissal and
Lil's recruitment. Opaque scene event R0003 (`95 46 7D 80 29 63 05 05 2C 63`)
stays unchanged. Employer and attendant presentation states `94` and `73`,
both `FI` name macros, and the `FA` name macro are preserved. The exact-font
previews show every first glyph; the narrow striped `W` was checked in
individual previews. See `docs/lil_sc2_b154_control_note.md`.

`out/all_routes_unified_lil_v61_candidate.nds`, SHA-256
`edee2e49b136c0623e725b7c445a23c7e43a6012a143f537d01ac9dc5534dfe3`,
uses `all-routes-unified-v27` with 328 experimental batches over the
unchanged accepted base. All 13 build checks, 41 focused tests, Ruff, the
baseline invariant, and saved-ROM verification pass. The ROM contains
19,217 exact experimental route records and 202 unchanged exclusions.
See `docs/all_routes_unified_lil_v61_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
3,507/6,608 translated, 3,068 remaining and 33 excluded. Continue B155.

## Experimental four-route Lil V62 candidate

B155 adds 48 source-reviewed natural-English records for Angelo Puccini's
recruitment and his African trade lesson. Opaque scene event R0059
(`20 31 46 EA 80`) stays unchanged. The five `FI` and one `FA` name macros
and all dialogue presentation leads are preserved. All exact-font previews
were reviewed. See `docs/lil_sc2_b155_control_note.md`.

`out/all_routes_unified_lil_v62_candidate.nds`, SHA-256
`ebb280764fe9f7c4ea252caf27c4e3de474b20ce756745994ad31e49f81be563`,
uses `all-routes-unified-v28` with 329 experimental batches over the
unchanged accepted base. All 13 build checks, 42 focused tests, Ruff, the
baseline invariant, and saved-ROM verification pass. The ROM contains
19,265 exact experimental route records and 203 unchanged exclusions.
See `docs/all_routes_unified_lil_v62_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
3,555/6,608 translated, 3,019 remaining and 34 excluded. Continue B156.

## Experimental four-route Lil V63 candidate

B156 adds all 69 source-reviewed natural-English records for Ian Dukov's
tavern dismissal, ambush, rescue, and recruitment. The tavern patron states
`A4` and `A5` and both `FI` name macros are preserved. All exact-font
previews were reviewed. See `docs/lil_sc2_b156_control_note.md`.

`out/all_routes_unified_lil_v63_candidate.nds`, SHA-256
`966ac21eec3d4e725763388f3bbfd22fa1eb2b53fb53df88a9551fc23a91403b`,
uses `all-routes-unified-v29` with 330 experimental batches over the
unchanged accepted base. All 13 build checks, 43 focused tests, Ruff, the
baseline invariant, and saved-ROM verification pass. The ROM contains
19,334 exact experimental route records and 203 unchanged exclusions.
See `docs/all_routes_unified_lil_v63_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
3,624/6,608 translated, 2,950 remaining and 34 excluded. Continue B157.

## Experimental four-route Lil V64 candidate

B157 adds all 70 source-reviewed natural-English records for Carlo Sinato's
market encounter, discovery of Adil's illness, family grief, and recruitment.
The `69` merchant, `8E` wife, and `FE` narration presentation states and both
`FI` name macros are preserved. All exact-font previews were reviewed. See
`docs/lil_sc2_b157_control_note.md`.

`out/all_routes_unified_lil_v64_candidate.nds`, SHA-256
`4f6075f090e81dcefbfafa52c2517d52da760551602a8abdca69ef6eb0246665`,
uses `all-routes-unified-v30` with 331 experimental batches over the
unchanged accepted base. All 13 build checks, 44 focused tests, Ruff, the
baseline invariant, and saved-ROM verification pass. The ROM contains
19,404 exact experimental route records and 203 unchanged exclusions.
See `docs/all_routes_unified_lil_v64_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
3,694/6,608 translated, 2,880 remaining and 34 excluded. Continue B158.

## Experimental four-route Lil V65 candidate

B158 adds all 19 source-reviewed natural-English records for Christina's
tavern dance, audience cheers, and crew reactions. The `FE` audience
presentation state and `FI` name macro are preserved. Both exact-font sheets
were reviewed. See `docs/lil_sc2_b158_control_note.md`.

`out/all_routes_unified_lil_v65_candidate.nds`, SHA-256
`57f85d6620cb13ed611715541ea983cc9a3ce55e8c804fda2bcd64cc9edc617b`,
uses `all-routes-unified-v31` with 332 experimental batches over the
unchanged accepted base. All 13 build checks, 45 focused tests, Ruff, the
baseline invariant, and saved-ROM verification pass. The ROM contains
19,423 exact experimental route records and 203 unchanged exclusions.
See `docs/all_routes_unified_lil_v65_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
3,713/6,608 translated, 2,861 remaining and 34 excluded. Continue B159.

## Experimental four-route Lil V66 candidate

B159 adds 41 source-reviewed natural-English records for Samwell's
elephant-market encounter, cooking test, and recruitment. Opaque scene event
R0045 (`21 51 46 EE 80`) stays unchanged. All four `FI` name macros and
speaker presentation leads are preserved. All exact-font previews were
reviewed. See `docs/lil_sc2_b159_control_note.md`.

`out/all_routes_unified_lil_v66_candidate.nds`, SHA-256
`0f20240c781e5b25bbbf6f99f85fe978738f24db6789c955f1303a41b3010829`,
uses `all-routes-unified-v32` with 333 experimental batches over the
unchanged accepted base. All 13 build checks, 46 focused tests, Ruff, the
baseline invariant, and saved-ROM verification pass. The ROM contains
19,464 exact experimental route records and 204 unchanged exclusions.
See `docs/all_routes_unified_lil_v66_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
3,754/6,608 translated, 2,819 remaining and 35 excluded. Continue B160.

## Experimental four-route Lil V67 candidate

B160-B162 add 23 source-reviewed natural-English records for the stolen-ship
discovery and two dockworker updates. All six source speaker presentation
leads, including new dockworker lead `74`, and the `FI` name macro are
preserved. All three exact-font previews were reviewed. See
`docs/lil_sc2_b160_b162_control_note.md`.

`out/all_routes_unified_lil_v67_candidate.nds`, SHA-256
`f84bf5dbca401d6d34f28d5fd798a14882c506db9152e3e3e0aa091bdd75008e`,
uses `all-routes-unified-v33` with 334 experimental batches over the
unchanged accepted base. All 13 build checks, 47 focused tests, Ruff, the
baseline invariant, and saved-ROM verification pass. The ROM contains
19,487 exact experimental route records and 204 unchanged exclusions.
See `docs/all_routes_unified_lil_v67_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
3,777/6,608 translated, 2,796 remaining and 35 excluded. Continue B163.

## Experimental four-route Lil V68 candidate

B163 adds 43 source-reviewed natural-English records for the ship's return
and Jam Jack Ludwyan's recruitment. Opaque seven-byte ship-return event
R0034 (`20 95 46 E2 80 2C 63`) stays unchanged. The `FI` name macro and
all speaker presentation leads are preserved. All three exact-font previews
were reviewed. See `docs/lil_sc2_b163_control_note.md`.

`out/all_routes_unified_lil_v68_candidate.nds`, SHA-256
`0bac7acc4b9dd8ac164043882f02e1a858d65126a5319a1076be4594e2b18229`,
uses `all-routes-unified-v34` with 335 experimental batches over the
unchanged accepted base. All 13 build checks, 48 focused tests, Ruff, the
baseline invariant, and saved-ROM verification pass. The ROM contains
19,530 exact experimental route records and 205 unchanged exclusions.
See `docs/all_routes_unified_lil_v68_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
3,820/6,608 translated, 2,752 remaining and 36 excluded. Continue B168.

## Experimental four-route Lil V69 candidate

B168 adds 52 source-reviewed natural-English records for Mikhail Lett's
recruitment and the item-information tutorial. All seven `FI`, one `FA`,
and one `FO` name macros and all nine speaker presentation leads are
preserved. All three exact-font previews were reviewed. See
`docs/lil_sc2_b168_control_note.md`.

`out/all_routes_unified_lil_v69_candidate.nds`, SHA-256
`8b3ce57b83b3276cca342b2026328301ec5dd6a446d3615c0958262ef3ea3a91`,
uses `all-routes-unified-v35` with 336 experimental batches over the
unchanged accepted base. All 13 build checks, 49 focused tests, Ruff, the
baseline invariant, and saved-ROM verification pass. The ROM contains
19,582 exact experimental route records and 205 unchanged exclusions.
See `docs/all_routes_unified_lil_v69_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
3,872/6,608 translated, 2,700 remaining and 36 excluded. Continue B169.

## Experimental four-route Lil V70 candidate

B169 adds 36 source-reviewed natural-English records for Mikhail's Proof
of Conqueror explanation and search advice. Five `FI` and two `FO` name
macros and all six speaker presentation leads are preserved. Both
exact-font previews were reviewed. See `docs/lil_sc2_b169_control_note.md`.

`out/all_routes_unified_lil_v70_candidate.nds`, SHA-256
`61cf07962603ba16240375636afc0596dbae239f3274af8952aa12074cb12ec3`,
uses `all-routes-unified-v36` with 337 experimental batches over the
unchanged accepted base. All 13 build checks, 50 focused tests, Ruff, the
baseline invariant, and saved-ROM verification pass. The ROM contains
19,618 exact experimental route records and 205 unchanged exclusions.
See `docs/all_routes_unified_lil_v70_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
3,908/6,608 translated, 2,664 remaining and 36 excluded. Continue B170.

## Experimental four-route Lil V71 candidate

B170 adds 33 source-reviewed natural-English records for Yifa's first
meeting with Lil and her recruitment. The `FI` and `FO` name macros and
both speaker presentation leads are preserved. Both exact-font previews
were reviewed. See `docs/lil_sc2_b170_control_note.md`.

`out/all_routes_unified_lil_v71_candidate.nds`, SHA-256
`e65b758e900ef87e8c09ef62c2669d71b3943673ec028a4187e058879e51a4a5`,
uses `all-routes-unified-v37` with 338 experimental batches over the
unchanged accepted base. All 13 build checks, 51 focused tests, Ruff, the
baseline invariant, and saved-ROM verification pass. The ROM contains
19,651 exact experimental route records and 205 unchanged exclusions.
See `docs/all_routes_unified_lil_v71_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
3,941/6,608 translated, 2,631 remaining and 36 excluded. Continue B171.

## Experimental four-route Lil V72 candidate

B171 adds 35 source-reviewed natural-English records for Sanghyeon's
dream visit and Yifa's renewed training. The `FI` name macro and all
speaker presentation leads, including new `51` Sanghyeon, are preserved.
Both exact-font previews were reviewed. See
`docs/lil_sc2_b171_control_note.md`.

`out/all_routes_unified_lil_v72_candidate.nds`, SHA-256
`4ada99bfa978d7f3bd34de53aaea180e787668f684ca39c633acbe483420ae3d`,
uses `all-routes-unified-v38` with 339 experimental batches over the
unchanged accepted base. All 13 build checks, 52 focused tests, Ruff, the
baseline invariant, and saved-ROM verification pass. The ROM contains
19,686 exact experimental route records and 205 unchanged exclusions.
See `docs/all_routes_unified_lil_v72_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
3,976/6,608 translated, 2,596 remaining and 36 excluded. Continue B172.

## Experimental four-route Lil V73 candidate

B172 adds 27 source-reviewed natural-English records for Julian and
Mihwa's Golden Crown of Silla lead. All three speaker presentation leads,
including new `C9` Mihwa, are preserved. Both exact-font previews were
reviewed. See `docs/lil_sc2_b172_control_note.md`.

`out/all_routes_unified_lil_v73_candidate.nds`, SHA-256
`fb4b21406ca7524b13491f413d895fdfcee1ac8108ba253403ce3b7c54003308`,
uses `all-routes-unified-v39` with 340 experimental batches over the
unchanged accepted base. All 13 build checks, 53 focused tests, Ruff, the
baseline invariant, and saved-ROM verification pass. The ROM contains
19,713 exact experimental route records and 205 unchanged exclusions.
See `docs/all_routes_unified_lil_v73_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,003/6,608 translated, 2,569 remaining and 36 excluded. Continue B173.

## Experimental four-route Lil V74 candidate

B173-B174 add 44 source-reviewed natural-English records for the Golden
Crown of Silla tomb lead, Mihwa's crown handoff, and Julian's recruitment.
All five speaker presentation leads, including new `CA` Seoul tavernkeeper,
are preserved. All three exact-font previews were reviewed. See
`docs/lil_sc2_b173_b174_control_note.md`.

`out/all_routes_unified_lil_v74_candidate.nds`, SHA-256
`1d1088494e40021a7b517e7c2bb784c545a6a0fb931e137d74ee5e5895a4ff25`,
uses `all-routes-unified-v40` with 341 experimental batches over the
unchanged accepted base. All 13 build checks, 54 focused tests, Ruff, the
baseline invariant, and saved-ROM verification pass. The ROM contains
19,757 exact experimental route records and 205 unchanged exclusions.
See `docs/all_routes_unified_lil_v74_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,047/6,608 translated, 2,525 remaining and 36 excluded. Continue B175.

## Experimental four-route Lil V75 candidate

B175 adds 32 source-reviewed natural-English dialogue records for Aziza's
pirate confrontation and Lil's sword rivalry. The four-byte `96 46 CA 80`
event payload is excluded unchanged. All six dialogue presentation leads
and four `FI` plus one `FA` name-macro instances are preserved. Both
exact-font previews were reviewed. See `docs/lil_sc2_b175_control_note.md`.

`out/all_routes_unified_lil_v75_candidate.nds`, SHA-256
`5471bfcb04fa891503a572dcc2d0797d520a76671cfb2e3f559384bf5c48b55b`,
uses `all-routes-unified-v41` with 342 experimental batches over the
unchanged accepted base. All 13 build checks, 55 focused tests, Ruff, the
baseline invariant, and saved-ROM verification pass. The ROM contains
19,789 exact experimental route records and 206 unchanged exclusions.
See `docs/all_routes_unified_lil_v75_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,079/6,608 translated, 2,492 remaining and 37 excluded. Continue B176.

## Experimental four-route Lil V76 candidate

B176 adds 10 source-reviewed natural-English records for the Seville
banana boom. The newly observed `AE` patron and `AF` attendant presentation
states are preserved. The exact-font preview was reviewed. See
`docs/lil_sc2_b176_control_note.md`.

`out/all_routes_unified_lil_v76_candidate.nds`, SHA-256
`415861f10fab2cb4ea2da0a50f2d50dc506067a8b2091e763ef05ec4fcbfa582`,
uses `all-routes-unified-v42` with 343 experimental batches over the
unchanged accepted base. All 13 build checks, 56 focused tests, Ruff, the
baseline invariant, and saved-ROM verification pass. The ROM contains
19,799 exact experimental route records and 206 unchanged exclusions.
See `docs/all_routes_unified_lil_v76_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,089/6,608 translated, 2,482 remaining and 37 excluded. Continue B177.

## Experimental four-route Lil V77 candidate

B177 adds 10 source-reviewed natural-English records for the Genoa
tomato boom. The `AE` patron, `AF` attendant, and `FE` market notice
presentation states are preserved. The exact-font preview was reviewed.
See `docs/lil_sc2_b177_control_note.md`.

`out/all_routes_unified_lil_v77_candidate.nds`, SHA-256
`1032a6defbcf0ff794f223e53751206737985936bb11a0844bbcdffab94c57a6`,
uses `all-routes-unified-v43` with 344 experimental batches over the
unchanged accepted base. All 13 build checks, 57 focused tests, Ruff, the
baseline invariant, and saved-ROM verification pass. The ROM contains
19,809 exact experimental route records and 206 unchanged exclusions.
See `docs/all_routes_unified_lil_v77_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,099/6,608 translated, 2,472 remaining and 37 excluded. Continue B178.

## Experimental four-route Lil V78 candidate

B178 adds 13 source-reviewed natural-English records for the Amsterdam
wheat boom. The three neighbors' `A6`-`A8` and `FE` market notice
presentation states are preserved. The exact-font preview was reviewed.
See `docs/lil_sc2_b178_control_note.md`.

`out/all_routes_unified_lil_v78_candidate.nds`, SHA-256
`2a0e5326680d90089171def03699994bcea233769003d7c7eb972a9801475314`,
uses `all-routes-unified-v44` with 345 experimental batches over the
unchanged accepted base. All 13 build checks, 58 focused tests, Ruff, the
baseline invariant, and saved-ROM verification pass. The ROM contains
19,822 exact experimental route records and 206 unchanged exclusions.
See `docs/all_routes_unified_lil_v78_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,112/6,608 translated, 2,459 remaining and 37 excluded. Continue B179.

## Experimental four-route Lil V79 candidate

B179 adds eight source-reviewed natural-English records for the San Jorge
wine boom. The `60` drinker, `5C` barkeep, and `FE` market notice
presentation states are preserved. The exact-font preview was reviewed.
See `docs/lil_sc2_b179_control_note.md`.

`out/all_routes_unified_lil_v79_candidate.nds`, SHA-256
`956b67826a86f38c1eb818506fb1c06a89745c0ae190ec92f1427275a4965e14`,
uses `all-routes-unified-v45` with 346 experimental batches over the
unchanged accepted base. All 13 build checks, 59 focused tests, Ruff, the
baseline invariant, and saved-ROM verification pass. The ROM contains
19,830 exact experimental route records and 206 unchanged exclusions.
See `docs/all_routes_unified_lil_v79_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,120/6,608 translated, 2,451 remaining and 37 excluded. Continue B180.

## Experimental four-route Lil V80 candidate

B180-B182 add 29 source-reviewed natural-English records for Lisbon spice,
Athens ruby, and London gem market rumors. The `A6`-`A8` townspeople and
`FE` market notice presentation states are preserved. Both exact-font
previews were reviewed. See `docs/lil_sc2_b180_b182_control_note.md`.

`out/all_routes_unified_lil_v80_candidate.nds`, SHA-256
`f48e9c0b728d176aa54dfecf3f7d8369121ae9eabe85b73f297d453044f3f6eb`,
uses `all-routes-unified-v46` with 347 experimental batches over the
unchanged accepted base. All 13 build checks, 60 focused tests, Ruff, the
baseline invariant, and saved-ROM verification pass. The ROM contains
19,859 exact experimental route records and 206 unchanged exclusions.
See `docs/all_routes_unified_lil_v80_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,149/6,608 translated, 2,422 remaining and 37 excluded. Continue B183.

## Experimental four-route Lil V81 candidate

B183 adds 25 source-reviewed natural-English records for the Basra
painting craze. The `99` short interjection, `94`, `6E`, and `84`
collectors, `55` shopkeeper, and `FE` door cue and market notice retain
their presentation states. Both exact-font previews were reviewed. See
`docs/lil_sc2_b183_control_note.md`.

`out/all_routes_unified_lil_v81_candidate.nds`, SHA-256
`39591ee8647471d035bc0f6782b7bb261849b0f43fd69ccd1cb7b6d97e861bb2`,
uses `all-routes-unified-v47` with 348 experimental batches over the
unchanged accepted base. All 13 build checks, 61 focused tests, Ruff, the
baseline invariant, and saved-ROM verification pass. The ROM contains
19,884 exact experimental route records and 206 unchanged exclusions.
See `docs/all_routes_unified_lil_v81_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,174/6,608 translated, 2,397 remaining and 37 excluded. Continue B184.

## Experimental four-route Lil V82 candidate

B184-B186 add 29 source-reviewed natural-English records for the Sofala
tea, Stockholm fur, and Alexandria sweets market scenes. The `A4`, `A5`,
`AE`, `AF`, and `FE` presentation states are preserved. Both exact-font
previews were reviewed. See `docs/lil_sc2_b184_b186_control_note.md`.

`out/all_routes_unified_lil_v82_candidate.nds`, SHA-256
`81997a3f6e70e5db51b80caff9f4e2754cac66329fca5f586c79a8e75cbcee24`,
uses `all-routes-unified-v48` with 349 experimental batches over the
unchanged accepted base. All 13 build checks, 62 focused tests, Ruff, the
baseline invariant, and saved-ROM verification pass. The ROM contains
19,913 exact experimental route records and 206 unchanged exclusions.
See `docs/all_routes_unified_lil_v82_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,203/6,608 translated, 2,368 remaining and 37 excluded. Continue B187.

## Experimental four-route Lil V83 candidate

B187 adds 16 source-reviewed natural-English records for the Malacca
almond-medicine rumor. The `9B` coughing man, `57` friend, and `FE` notice
preserve their presentation states. The exact-font contact sheet was
reviewed. See `docs/lil_sc2_b187_control_note.md`.

`out/all_routes_unified_lil_v83_candidate.nds`, SHA-256
`bda5947b7e2418e6f2690bbb1bab565b65d49031ec9b4274f5ef9efaa7faca8e`,
uses `all-routes-unified-v49` with 350 experimental batches over the
unchanged accepted base. All 13 build checks, 37 focused stack tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
19,929 exact experimental route records and 206 unchanged exclusions.
See `docs/all_routes_unified_lil_v83_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,219/6,608 translated, 2,352 remaining and 37 excluded. Continue B188.

## Experimental four-route Lil V84 candidate

B188 adds 11 source-reviewed natural-English records for the Osaka
giyaman-glass market rumor. Source-leading `82` and `96` are Shift-JIS text
leads, so English first letters remain visible; `FE` is the market notice.
The exact-font contact sheet was reviewed. See
`docs/lil_sc2_b188_control_note.md`.

`out/all_routes_unified_lil_v84_candidate.nds`, SHA-256
`5447d57ae45273393a4c3e99d61892b883a712c2f7f4a499ac80a65e9befac66`,
uses `all-routes-unified-v50` with 351 experimental batches over the
unchanged accepted base. All 13 build checks, 38 focused stack tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
19,940 exact experimental route records and 206 unchanged exclusions.
See `docs/all_routes_unified_lil_v84_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,230/6,608 translated, 2,341 remaining and 37 excluded. Continue B189.

## Experimental four-route Lil V85 candidate

B189 adds 17 source-reviewed natural-English records for the Hamburg
ceramics collectors and swindlers. Source-correlated `93`/`52` collectors,
`68`/`71` swindlers, and `FE` market notice retain their presentation states.
The exact-font contact sheet was reviewed. See
`docs/lil_sc2_b189_control_note.md`.

`out/all_routes_unified_lil_v85_candidate.nds`, SHA-256
`3ba11db1411ea310290bd14238e84c13c8b2b4fb1f7f61b96efefd4006cbf1fc`,
uses `all-routes-unified-v51` with 352 experimental batches over the
unchanged accepted base. All 13 build checks, 39 focused stack tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
19,957 exact experimental route records and 206 unchanged exclusions.
See `docs/all_routes_unified_lil_v85_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,247/6,608 translated, 2,324 remaining and 37 excluded. Continue B190.

## Experimental four-route Lil V86 candidate

B190 adds 17 source-reviewed natural-English records for the Havana
medicine rumor. Source-correlated `9F`/`77` speakers and the `FE` notice
retain their presentation states. The exact-font contact sheet was
reviewed. See `docs/lil_sc2_b190_control_note.md`.

`out/all_routes_unified_lil_v86_candidate.nds`, SHA-256
`beeac8e92bc9ddb37d0d06463d586f5c37687d16f9cd26ca7f4918c75128cb68`,
uses `all-routes-unified-v52` with 353 experimental batches over the
unchanged accepted base. All 13 build checks, 40 focused stack tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
19,974 exact experimental route records and 206 unchanged exclusions.
See `docs/all_routes_unified_lil_v86_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,264/6,608 translated, 2,307 remaining and 37 excluded. Continue B191.

## Experimental four-route Lil V87 candidate

B191 adds 13 source-reviewed natural-English records for the Calicut
father-son dye-market conversation. Source-correlated `56`/`9A` speakers
and the `FE` notice retain their presentation states. The exact-font
contact sheet was reviewed. See `docs/lil_sc2_b191_control_note.md`.

`out/all_routes_unified_lil_v87_candidate.nds`, SHA-256
`fd74d912742508d952187bc9330ae6057ceb10e485c58773094bb7de3f6bdce9`,
uses `all-routes-unified-v53` with 354 experimental batches over the
unchanged accepted base. All 13 build checks, 41 focused stack tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
19,987 exact experimental route records and 206 unchanged exclusions.
See `docs/all_routes_unified_lil_v87_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,277/6,608 translated, 2,294 remaining and 37 excluded. Continue B192.

## Experimental four-route Lil V88 candidate

B192-B194 add 33 source-reviewed natural-English records for Istanbul
tobacco, Seoul chili peppers, and Hangzhou sake. The Hangzhou `9C`/`75`
states and companion `FI` name macro are preserved. Exact-font review caught
the boxed fullwidth `Ｉ` workaround in the Istanbul notice; Lil's text now
uses `Constantinople` and renders cleanly. See
`docs/lil_sc2_b192_b194_control_note.md`.

`out/all_routes_unified_lil_v88_candidate.nds`, SHA-256
`e71492a8b922fdd46e951bca382e492f89daf35679772f114e56b4e2ef8a6fc2`,
uses `all-routes-unified-v54` with 355 experimental batches over the
unchanged accepted base. All 13 build checks, 42 focused stack tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
20,020 exact experimental route records and 206 unchanged exclusions.
See `docs/all_routes_unified_lil_v88_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,310/6,608 translated, 2,261 remaining and 37 excluded. Continue B195.

## Experimental four-route Lil V89 candidate

B195 adds 20 source-reviewed natural-English records for the Veracruz
cheese-dish market scene. Source-correlated `77`/`67` patrons, `5C` barkeep,
and `FE` market notice retain their presentation states. The exact-font
contact sheet was reviewed. See `docs/lil_sc2_b195_control_note.md`.

`out/all_routes_unified_lil_v89_candidate.nds`, SHA-256
`ee2fcb4905b723d48b861272dff6872699badeb240f17250c2d335911b01c379`,
uses `all-routes-unified-v55` with 356 experimental batches over the
unchanged accepted base. All 13 build checks, 43 focused stack tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
20,040 exact experimental route records and 206 unchanged exclusions.
See `docs/all_routes_unified_lil_v89_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,330/6,608 translated, 2,241 remaining and 37 excluded. Continue B196.

## Experimental four-route Lil V90 candidate

B196 adds 35 source-reviewed natural-English records for all six haggling
stages, Buy/Pass choices, crew advice, sale outcomes, and the `FI` charm
reward. Source-leading `94` is Shift-JIS choice text here and is removed
from this batch's speaker-state profile, preserving every English choice
initial. Both exact-font contact sheets were reviewed. See
`docs/lil_sc2_b196_control_note.md`.

`out/all_routes_unified_lil_v90_candidate.nds`, SHA-256
`dd2557ee21672476b698f5c5ef7e72bd26ff6d9d313c07e783c66a376c6abc21`,
uses `all-routes-unified-v56` with 357 experimental batches over the
unchanged accepted base. All 13 build checks, 44 focused stack tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
20,075 exact experimental route records and 206 unchanged exclusions.
See `docs/all_routes_unified_lil_v90_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,365/6,608 translated, 2,206 remaining and 37 excluded. Continue B197.

## Experimental four-route Lil V91 candidate

B197 adds 24 source-reviewed natural-English text records for Ian's
celestial-maiden book offer, all Buy it/Pass/Trust choices, purchase and gift
branches, and his charm reward. One four-byte packed portrait/scene payload
is excluded unchanged. Source-leading `94` is Shift-JIS choice text, and the
batch profile keeps it out of the speaker-state set so each English first
letter survives. Both exact-font contact sheets were reviewed. See
`docs/lil_sc2_b197_control_note.md`.

`out/all_routes_unified_lil_v91_candidate.nds`, SHA-256
`8df467e1f92f5b6012033d98e8d763e18ca6b28418a9bd105a379ab24da5e9b3`,
uses `all-routes-unified-v57` with 358 experimental batches over the
unchanged accepted base. All 13 build checks, 45 focused stack tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
20,099 exact experimental route records and 207 unchanged exclusions.
See `docs/all_routes_unified_lil_v91_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,389/6,608 translated, 2,181 remaining and 38 excluded. Continue B198.

## Experimental four-route Lil V92 candidate

B198 adds all 15 source-reviewed natural-English namahage-dream records,
including Yukihisa's discovery and his plan to hand the object to the
admiral. `FE`, `0C`, and `0F` presentation states are retained. Both
exact-font contact sheets were reviewed, with all first glyphs intact.
See `docs/lil_sc2_b198_control_note.md`.

`out/all_routes_unified_lil_v92_candidate.nds`, SHA-256
`b6855ac0e500396de4403b68a53d198f1c1d8e5544a0783668f5616a3c86312f`,
uses `all-routes-unified-v58` with 359 experimental batches over the
unchanged accepted base. All 13 build checks, 46 focused stack tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
20,114 exact experimental route records and 207 unchanged exclusions.
See `docs/all_routes_unified_lil_v92_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,404/6,608 translated, 2,166 remaining and 38 excluded. Continue B199.

## Experimental four-route Lil V93 candidate

B199 adds 31 source-reviewed natural-English text records for Samwell and
Kamil at Rocco Alemkel's portrait, Lil's chase, the old-book discovery, and
the mistaken gift. One four-byte packed item/scene payload is excluded
unchanged. `16`, `09`, `02`, and `FE` states and the live `FI` admiral-name
macro are retained. Four exact-font contact sheets were reviewed. See
`docs/lil_sc2_b199_control_note.md`.

`out/all_routes_unified_lil_v93_candidate.nds`, SHA-256
`3cf1abde5319d6638df4385d5fb4ba1bb2cf605f03d0b78fc42fe773160c4568`,
uses `all-routes-unified-v59` with 360 experimental batches over the
unchanged accepted base. All 13 build checks, 47 focused stack tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
20,145 exact experimental route records and 208 unchanged exclusions.
See `docs/all_routes_unified_lil_v93_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,435/6,608 translated, 2,134 remaining and 39 excluded. Continue B200.

## Experimental four-route Lil V94 candidate

B200 adds all 19 source-reviewed natural-English records for Carlo's rescue
of a collapsed traveler, the inn conversation, gift, and charm reward. The
traveler's `AC` presentation state is added; Carlo's `13` and `FE` notices
are retained. Both exact-font contact sheets were reviewed. See
`docs/lil_sc2_b200_control_note.md`.

`out/all_routes_unified_lil_v94_candidate.nds`, SHA-256
`a14e61e108a3dbaeb4213c1fd96d68a158f8ae1c6fe1247dc5cdd929148f138a`,
uses `all-routes-unified-v60` with 361 experimental batches over the
unchanged accepted base. All 13 build checks, 48 focused stack tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
20,164 exact experimental route records and 208 unchanged exclusions.
See `docs/all_routes_unified_lil_v94_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,454/6,608 translated, 2,115 remaining and 39 excluded. Continue B201.

## Experimental four-route Lil V95 candidate

B201 adds all 25 source-reviewed natural-English mast-rope bargaining
records: every price and counteroffer, Buy/Pass choices, purchase and refusal,
and the charm, wit, and spirit rewards. Choice-leading `94` remains Shift-JIS
text, so the English initials are preserved; both `FI` admiral-name macros
remain live. Three exact-font contact sheets were reviewed. See
`docs/lil_sc2_b201_control_note.md`.

`out/all_routes_unified_lil_v95_candidate.nds`, SHA-256
`aae7c7ba924d706b85106961f7d470797b5fcbbd327cdac0aec6863fb489ed12`,
uses `all-routes-unified-v61` with 362 experimental batches over the
unchanged accepted base. All 13 build checks, 49 focused stack tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
20,189 exact experimental route records and 208 unchanged exclusions.
See `docs/all_routes_unified_lil_v95_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,479/6,608 translated, 2,090 remaining and 39 excluded. Continue B202.

## Experimental four-route Lil V96 candidate

B202 adds all 19 source-reviewed natural-English records for the fleeing
stranger's Glassmaking Guide handoff, the pursuer, Lil's confusion, and
Charles's book request. The stranger's `9D` presentation state is added;
`93`, `02`, and `12` are retained. Both exact-font contact sheets were
reviewed. See `docs/lil_sc2_b202_control_note.md`.

`out/all_routes_unified_lil_v96_candidate.nds`, SHA-256
`ecead7922f7c2123ec85ff0f5567311d398300747fe95f7402f094cd61e95356`,
uses `all-routes-unified-v62` with 363 experimental batches over the
unchanged accepted base. All 13 build checks, 50 focused stack tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
20,208 exact experimental route records and 208 unchanged exclusions.
See `docs/all_routes_unified_lil_v96_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,498/6,608 translated, 2,071 remaining and 39 excluded. Continue B203.

## Experimental four-route Lil V97 candidate

B203 adds all 21 source-reviewed natural-English records for Mikhail and
Lil's caterpillar-fungus discovery, the herbalist's medicine book, the
1,000-to-100-coin exchange, and the `FI` charm reward. `4C`, `02`, `AA`,
and `FE` presentation states remain intact. Three exact-font contact sheets
were reviewed. See `docs/lil_sc2_b203_control_note.md`.

`out/all_routes_unified_lil_v97_candidate.nds`, SHA-256
`4699e527c9d3e17b84d7882dce7619ea90776a8b8b9b76bdff3f3e1144bce9d3`,
uses `all-routes-unified-v63` with 364 experimental batches over the
unchanged accepted base. All 13 build checks, 51 focused stack tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
20,229 exact experimental route records and 208 unchanged exclusions.
See `docs/all_routes_unified_lil_v97_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,519/6,608 translated, 2,050 remaining and 39 excluded. Continue B204.

## Experimental four-route Lil V98 candidate

B204 adds all 20 source-reviewed natural-English records for Jam's Japanese
castle visit, mistaken shachihoko figurehead, the retainer's report, the
lord's search order, and Jam's signed letter. The `91`, `7C`, and `82`
presentation states are added; `0B`, `02`, and `FE` remain intact. Both
exact-font contact sheets were reviewed. See
`docs/lil_sc2_b204_control_note.md`.

`out/all_routes_unified_lil_v98_candidate.nds`, SHA-256
`cd9a95e3a113c39787dfec6a542fc786d5e402177d0d3366ccfb3ee2bbbb293a`,
uses `all-routes-unified-v64` with 365 experimental batches over the
unchanged accepted base. All 13 build checks, 52 focused stack tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
20,249 exact experimental route records and 208 unchanged exclusions.
See `docs/all_routes_unified_lil_v98_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,539/6,608 translated, 2,030 remaining and 39 excluded. Continue B205.

## Experimental four-route Lil V99 candidate

B205 adds 17 source-reviewed natural-English records for Angelo and Lil's
talking-parrot encounter and preserves one packed event payload unchanged.
The parrot repeats Angelo's words without unsafe uppercase renderer bytes.
Both exact-font contact sheets were reviewed. See
`docs/lil_sc2_b205_control_note.md`.

`out/all_routes_unified_lil_v99_candidate.nds`, SHA-256
`ef4be089c3f1b2200a3405e542d7b520bc4956a2438fc80d3d32200c55b6caa5`,
uses `all-routes-unified-v65` with 366 experimental batches over the
unchanged accepted base. All 13 build checks, 53 focused stack tests, Ruff,
the baseline invariant, and saved-ROM verification pass. The ROM contains
20,266 exact experimental route records and 209 unchanged exclusions.
See `docs/all_routes_unified_lil_v99_checkpoint.md`.

Runtime cold-boot and explicit acceptance remain pending. Lil coverage is
4,556/6,608 translated, 2,012 remaining and 40 excluded. Continue B206.

## Experimental four-route Lil V100 candidate

B206 adds 28 natural-English ceramic-earrings text and choice records with
one packed item payload excluded unchanged. The four bare choices keep their
first glyphs. All three contact sheets were reviewed, dialogue QA has zero
blockers, 54 focused tests and Ruff pass, and the build and saved-ROM checks
pass. See `docs/all_routes_unified_lil_v100_checkpoint.md`.

Candidate `out/all_routes_unified_lil_v100_candidate.nds`, SHA-256
`43809c90b4a59ff33382f61d3b6d66455c12d70fe26c90362062118e1a79b96c`,
contains 20,294 exact experimental route records and 210 unchanged exclusions.
Lil coverage is 4,584/6,608 translated, 1,983 remaining and 41 excluded.
Continue B207. Runtime cold-boot and explicit acceptance remain pending.

## Experimental four-route Lil V101 candidate

B207-B214 add 126 natural-English treasure-scene records, with all letter
variants and five choices, and preserve one packed sword event unchanged.
All 13 contact sheets, dialogue audit, 55 focused tests, Ruff, 13 build checks,
baseline invariant and saved-ROM verification pass. See
`docs/all_routes_unified_lil_v101_checkpoint.md`.

Candidate `out/all_routes_unified_lil_v101_candidate.nds`, SHA-256
`52f8926665e75694d5ad8d46c79c598f38fc4b05314eb21be87988de7b9eda97`,
contains 20,420 exact experimental route records and 211 unchanged exclusions.
Lil coverage is 4,710/6,608 translated, 1,856 remaining and 42 excluded.
Continue B215. Runtime cold-boot and explicit acceptance remain pending.

## Experimental four-route Lil V102 candidate

B215-B226 add 155 natural-English legend and armor records. All 16 sheets,
dialogue QA, 57 formatter tests, 56 Lil tests, Ruff, build checks, baseline
and saved-ROM verification pass. See `docs/all_routes_unified_lil_v102_checkpoint.md`.
Lil coverage is 4,865/6,608, with 1,701 remaining and 42 excluded. Continue B227.
Runtime cold-boot and explicit acceptance remain pending.

## Experimental four-route Lil V103 candidate

B227-B238 adds 166 verified natural-English records and no exclusions.
All 17 sheets, dialogue QA, 57 Lil tests, Ruff, build, baseline and saved-ROM
checks pass. See `docs/all_routes_unified_lil_v103_checkpoint.md`.
Coverage 5,031/6,608; 1,535 remaining; 42 excluded. Continue B239.
Runtime cold-boot and explicit acceptance remain pending.

## Experimental four-route Lil V104 candidate

B239-B249 adds 135 verified natural-English records and one unchanged packed
figurehead event. All 14 sheets, zero-blocker QA, 58 Lil tests, Ruff, build,
baseline and saved-ROM checks pass. See `docs/all_routes_unified_lil_v104_checkpoint.md`.
Coverage 5,166/6,608; 1,399 remaining; 43 excluded. Continue B250.
Runtime cold-boot and explicit acceptance remain pending.

## Experimental four-route Lil V105 candidate

B250-B254 adds 83 verified natural-English figurehead and puzzle records,
with one curse-control payload unchanged. All nine sheets, QA, 59 Lil tests,
Ruff, build, baseline and saved-ROM checks pass. See `docs/all_routes_unified_lil_v105_checkpoint.md`.
Coverage 5,249/6,608; 1,315 remaining; 44 excluded. Continue B255.
Runtime cold-boot and explicit acceptance remain pending.
