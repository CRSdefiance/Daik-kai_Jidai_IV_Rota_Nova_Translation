# V540 coin-game prompts and original board display

The previously unresolved full-screen SLACK image caller at 020640EC belongs
to the coin-taking game. Its original entry is 02063898. Main dispatch major
opcode 6, subopcode 1 reaches 02029410 and invokes that entry. The original
two-byte instruction is `01 C1`, preserved in clean SC0 block 178 at offset 388.

An isolated research fixture replaces the opening movie instruction in SC0
block 44 at offset 26 with that exact original instruction. All instruction
lengths, offsets, prose, other controls, art and components remain unchanged.
This exercises the original minigame widget but does not establish Fernando's
normal recruitment trigger. Its post-return story branch is not compatible
with the substituted opening and is excluded from testing.

## Newly found untranslated prompts

The first native screen showed Japanese that earlier graphics/cache checks had
not exposed. These are three ARM9 literal strings, separate from COMMON/SC prose.
Their complete source span is 145098–1450DC and their only pointer literals are
639EC, 639F0 and 639F4.

| Original | Localized English |
| --- | --- |
| 先攻後攻をきめようか | Let's decide who goes first. |
| あんたの番からだぜ | You go first. |
| 俺からいかせてもらうぜ | I'll go first. |

All three records have clean-source meaning, character context, localization
notes and individual natural-dialogue-v2 review gates. They remain single logical
paragraphs with no authored breaks or alignment spaces. Complete wording uses
64 of the original 68 owned bytes. Two literal pointers move within that span.
Every other byte, section extent, heap/startup/cache value and executable
instruction remains exact to V534.

## Actual display and preservation

- All three complete native font masks pass, including punctuation, leading and
  final letters, empty cells and absence of old glyphs beyond the new wording.
- The normal fixture displays the decision and player-first messages. A separately
  labeled data-pointer selection fixture displays the opponent-first message in
  the same original dialog path. Both real conditional selector fragments execute
  for supplied outcomes 0/1 and choose the correctly relocated message pointers.
  The alternate display does not prove a naturally generated opponent-first flip.
- The original `slackimg11.pxl` board displays on the lower screen through its
  intended minigame caller. All 12,672 independently unobscured pixels in
  (80,192)–(256,264) match the original source. Portraits, dialog boxes, coins and
  controls obscure other parts; a complete unobscured board is not claimed.
- Ordinary coin touch and A inputs change coin/selection visuals. No completed
  wager, normal recruitment or subsequent story branch is credited.
- All 56 title/New Game/story/town/Help frames match V534 exactly. All 470
  inherited batches, 114 accepted layers, 675 graphics files and 921 source
  preservation entries remain. Only ARM9 differs from production V534.
- The xdelta from `work/clean.nds` reconstructs V540 byte-for-byte.

The earlier broad "creature paintings" label for generic SLACK images 0–10 is
not an established identity for every picture. Use "generic story illustrations"
until each source event supplies its subject. The native pixel evidence and
retain-original-art decisions are unchanged by this terminology correction.

## Registered candidate

- Profile: `all-routes-unified-v540`.
- ROM: `out/all_routes_combined_v540_candidate.nds`.
- SHA-256: `9f2e4c47c059b0606141d93c0f17a34f16a75fd66ceefe63c04e8a2a54577859`.
- Base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Changed internal component versus V534: `/__arm9__.bin`, owned coin strings
  and two guarded literal pointers only.
- Status: experimental; canonical unchanged and not promoted.

The ROM, manifest, exact reconstructable patch and BUILD_NOTES_V540.md are
copied to `E:/Rota Nova translations`. Labeled native captures are archived under
`Screenshots/Test fixtures/coin_game_v540`.

## Reproduction and remaining scope

- `dk4tool/patch/coin_game_prompts.py` and registered builder stage.
- `translations/coin_game_prompt_manuscript_v1.json` and `coin_game_prompts_v1.json`.
- `scripts/prepare_coin_game_gpu_v539.py` for source-opcode research fixtures.
- `scripts/verify_coin_game_release_v540.py` for preservation, selectors, masks,
  board region, regression frames and patch reconstruction.
- `work/analysis/coin_game_v540/release_proof.json`, `preservation_proof.json`,
  fixture manifests and copy receipts.

All 22 original requirements and all 18 incomplete plaque/hint entries remain.
Raw legacy consumers, reconstruction beneath removed Japanese lettering and
other contexts remain open. The full graphics goal stays active. Revisit older
record-based checks at full completion.
