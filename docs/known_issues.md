# Known issues

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
