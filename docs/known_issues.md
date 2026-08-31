# Known issues

## Accepted COMMON gameplay baseline

The user explicitly promoted `out/common_gameplay_natural_v2_candidate.nds` on
2026-08-31. Its bytes are now the canonical
`out/raphael_natural_v2_accepted_base.nds`; the SHA-256 is
`c94e1fd7221c5e929c851a39f1e722c8b127992bea743dd9992ca1ff027afcdf`.
It is built from the immutable accepted Raphael baseline under profile
`common-gameplay-natural-v2`; its manifest and the independent verifier agree
that only the expected 14 interface, COMMON, and Hodram-first-Stockholm paths
changed. The full regression suite passes (242 tests).

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
mapped and translated in the corrected research candidate `out/sound_selector_en_v5.nds`:
38 BGM titles are packed across `/COMMON/MESFILE.DK4` block 36 records 46-63,
while 57 SFX titles occupy fixed or standalone ARM9 slots. The BGM panel uses a
packed interior-pointer table; replacing labels without remapping those pointers
produces fragmented and reordered words. V1 through V3 are therefore superseded.
V4 correctly remapped the titles but is revoked because its build command omitted the
accepted Options/UI batch, reverting the surrounding menu. V5 used the former
`sound-setup` release profile to apply Options/UI, SFX, and BGM together. Some titles
remain abbreviated to fit their original packed regions, and the user reported
additional bugs in V5. Sound Setup is paused; its profile is now `rebase-required` and
the integrated builder rejects it. Rebase all three dependent tables against the new
accepted parent before another candidate, and do not include the old sound batches in
unrelated builds.

## Lil opening scene control preamble

Lil's actual opening is `/data/SC2.DK4`, block 22. Its dialogue records begin
with control sequences that affect the active portrait and name plate. Replacing
the visible Japanese text while retaining only a guessed byte prefix produces an
incorrect speaker and corrupts the first visible English glyph.

`lil_sc2_opening_repair.nds` and `lil_sc2_opening_repair_v2.nds` are revoked
research candidates and must not be distributed. The safe integration baseline
is `out/raphael_natural_v2_accepted_base.nds`. Map the full control preamble in
a disposable live-tested probe before another SC2 block-22 translation build.

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
`Ardelknatts`. An audit of the other 196 shared personal-name and surname slots found
them already translated in the accepted baseline.

The shared tavern repair preserves each proven packed interior entry point while
fixing the reported bare price, lowercase diagnostic, empty Francisca response,
broken Clifford introduction, and terse rumor/strength lines. All new fixed-dialogue
records pass the natural-dialogue audit with no warnings or errors; packed records
have exact-offset regression tests.

Do not promote this ROM until a cold boot completes Hodram's opening and visits all
three first-Stockholm buildings. Test both tutorial choices, tavern purchases,
Francisca, sailor recruitment, nameplates, menus, wrapping, and every return to town.
# Revoked protected-newline probe (2026-08-14)

`out/dialogue_protected_newline_probe.nds` is revoked and must not be tested,
distributed, or used as a parent. Its helper overwrites live structured data at
`0x02172300`. `dialogue_live_safe_v3.nds` remains the safe dialogue baseline,
and protected `0A 20` breaks remain mandatory in translation data.
