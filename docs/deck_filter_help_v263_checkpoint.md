# Dialogue alignment and Deck View checkpoint V263

## User-requested dialogue margin

The illustrated Square Shopkeeper dialogue is fixed by the shared modal renderer
introduced in V258. First-line padding moves left6 pixels; continuation padding
is retained, so both lines start at x22. All526 native-font ink pixels in the exact
shopkeeper sentence survived its targeted cold boot. Five observed first rows
shifted with no letter loss, while48 other full captures were unchanged.
Intentional larger indentation, control prefixes and unsupported geometry retain
native behavior. See `common_dialogue_left_alignment_v258.md` and its before/after
sheet. The V263 profile preserves that exact alignment-v2 stage and all stored
story/COMMON strings. This V263 test visited a separate Deck View path; it does not
claim a fresh traversal of every shopkeeper or dialogue parent.

## Additional observed formatting correction

Actual Deck View exposed Japanese navigator filter choices 未配置 and 全員,
localized as **Unassigned** and **All**. Clean-source instructions now explain
room-dependent duties, required abilities, inability to assign without sufficient
ability, and improved effectiveness at higher ability. Logical English is stored
separately from compiler-produced protected word-boundary breaks.

V262 was revoked before handoff: the isolated model assumed12-pixel line spacing,
but actual help uses16 pixels and clipped the final ability sentence. V263 keeps
all source facts in complete natural English and displays every line. The actual
20800-frame ordinary DeSmuME cold boot verifies all2299 help ink pixels, all128
Unassigned pixels and all38 All pixels against the independent native font, with
complete first/final letters and no split words. Changed pixels compared to V262
are confined to ability help rows; all other pixels in every comparable frame are
preserved. 50 comparable full frames are identical.

The native test executes the original help consumer and font with captured parent
origins16/32/64 and height128 explicitly supplied. Its coordinate conversion bridge
and bitmap-clear bridge are contracts, not proof of the native parent conversion
or GPU clearing. The actual saved-ROM capture provides independent display proof.
Native boot/cache ownership, ARM7 source integrity, arena, guards and ABI checks
pass. This is targeted emulator verification, not a full playthrough/hardware test.

## Integrated candidate

| Item | Value |
|---|---|
| Candidate | `out/all_routes_combined_v263_candidate.nds` |
| ROM SHA256 | `bcadeaa31ba988ac81c13e33526de2d7c90791ffff2ff319fb507cfd958af9b2` |
| Patch | `out/all_routes_combined_v263_candidate.xdelta` |
| Patch SHA256 | `88d9d400567a80ff67478e4dd169983b65ecbffb9e23b962d3a9d2d5ee08e11b` |
| Profile | `all-routes-unified-v263` |
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Canonical SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch input | `work/clean.nds` |
| Clean SHA256 | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| Changed internal component versus V261 | ARM9 only |

All467 inherited accepted/experimental batches, required layers, previous stages
and changed records are retained; the neighboring manifest lists each. All game
files, story/COMMON records, artwork, ARM7 and overlays are exactV261. The shared
builder reproduces fullV261 byte-for-byte, and the clean-input xdelta reconstructs
V263 exactly. V262's failed layout remains reproducible through configuration
version1; V263 uses version2. Ruff passes changed scripts/module.

Experimental; canonical unchanged, explicit user cold-boot acceptance pending.
On the user's emulator, check title/New Game, an established dialogue scene,
Square Shopkeeper margins and complete letters, then Deck View help and Filter.
All18 plaque/hint entries, Armor/Weapon variants and the full graphics goal remain
incomplete. Regional Admiral's actual parent, other rank parents, occupied equipment,
Online source gaps, Gallery/native archive loading and broader contextual displays
remain open. Revisit older record-based checks at actual goal completion.
