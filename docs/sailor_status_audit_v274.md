# Sailor status source and display audit (V274 research)

This audit uses the unchanged registered **V272** ROM, SHA256
`e9757bebf055839831512c353fb5e5f934d2b3943fa39cf17333875276d0a8c8`.
V274 is an evidence checkpoint; no V274 ROM or patch was built.
The previous goal turn recorded the user's Online screenshot scope exception.
This turn adds status source/consumer evidence and fresh gameplay captures.

## Original source and native selection

The original Mood table is at `021483B0`; Health is at `021483C8`.
Native selectors `0207E070` and `0207E0BC` read actor bytes 7 and 6,
respectively. Selector code, table order and pointers are unchanged in V272.

| Field | State | Original | Current English | Meaning to preserve |
|---|---:|---|---|---|
| Mood | 0 | ハイ | High | Excited or elevated mood; review the ambiguous English label in its gameplay context. |
| Mood | 1 | 元気 | Good | Energetic, in good spirits. |
| Mood | 2 | リラックス | Relaxed | Relaxed. |
| Mood | 3 | 通常 | Normal | Ordinary mental condition. |
| Mood | 4 | 不機嫌 | Upset | Bad mood or irritability. |
| Mood | 5 | 混乱 | Dazed | Confusion; confirm that Dazed communicates the actual state accurately. |
| Health | 0 | 健康 | Healthy | Healthy. |
| Health | 1 | 疲労 | Tired | Fatigued. |
| Health | 2 | 軽傷 | Wounded | Minor injury. |
| Health | 3 | 重傷 | Injured | Serious injury; retain the distinction from minor injury. |
| Health | 4 | 瀕死 | Dying | Near death. |
| Health | 5 | 疾病 | Sick | Illness. |
| Health | 6 | 死亡 | Dead | Dead. |

The isolated native calls exercise every byte value for each field, in both the
original and current code: **1,024 selector cases**. Valid states return the exact
original table pointers; invalid states retain the original fallback behavior.
Actor input bytes, saved registers and stack are preserved. All 13 English strings
decode through the actual ROM font and fit within 48 pixels of advance width.
This does not prove the complete drawing pipeline for every alternate state.
No isolated fixture is injected into the running game.

## Fresh gameplay and complete displayed pixels

A **32,200-frame DeSmuME cold boot** uses ordinary controller/stylus input.
It completes Rafael's initial town tutorial, visits the Tavern, confirms the
340-coin Treat Everyone action and visits all four available Sailor Info screens.
It then uses Order Drink and revisits the captain. No savestate is loaded.

Treat Everyone leaves the four officers at **Healthy / Normal**; Order Drink
also leaves the captain at **Healthy / Normal**. These two ordinary paths did
not produce an alternate officer state. Do not repeat them as presumed ways to
obtain one. The displayed town balance is 29,660 after the round, then 29,655
after the drink; this audit makes no wider economy/arithmetic claim.

For the five final Sailor Info cases:

- All 10 complete status label composites match the independent native font,
  including every first and last letter: Healthy has 93 ink pixels and Normal 83.
- All 50 complete plaque regions match the integrated source art and palette.
- All 50 complete skill label/number lines match, including spaces and digits.
- Recorded PNG hashes and the actual ROM hash are verified.

Health text starts at `(56,108)`; Mood at `(56,128)`. Healthy's full cell bounds
are `[56,108,98,119]`; Normal's are `[56,128,92,139]`. Both lines use the same
left margin. The existing runtime captain name still says Raphael Castor;
the locked Rafael spelling remains a separate consistency requirement.

## Remaining work

All **18 plaque/hint audit entries and Armor/Weapon variants remain incomplete**,
as the user requested. Alternate-state gameplay, occupied weapon/armor contexts,
remaining native/art consumers, name consistency and final goal verification
remain open. The low-resolution Online images are excluded from further
translation by the user's 2026-10-10 instruction.

The next status investigation should follow original status-changing consumers.
`status_setter_callers.json` records 55 aligned direct ARM branch candidates with
nearby instructions, including explicit Tired/Relaxed/Upset/Dazed setters.
These are source-code leads, not proof of event identity or a complete call graph;
indirect/generated/overlay consumers are not excluded. Establish the normal game
action for a particular caller before relying on it for alternate-state evidence.
Review High, Dazed and injury severity labels against those contexts before
closing the translation review. Do not mark all 13 alternate displays verified
from native selector or font metrics alone.

The graphics goal is active and incomplete. Revisit older record-based checks
at eventual goal completion, including independent complete glyph pixels.

## Evidence

- `work/analysis/plaque_states_v274/status_table_proof.json`
- `work/analysis/plaque_states_v274/saved_display_proof.json`
- `work/analysis/plaque_states_v274/status_setter_callers.json`
- `work/emulation_v193/plaque_states_v274/capture_report.json`
- `scripts/verify_sailor_status_tables_v274.py`
- `scripts/verify_sailor_status_display_v274.py`

Both verification scripts pass, and Ruff passes both new Python files.
The emulator process exited successfully. This is a targeted emulator test,
not a complete route playthrough or physical-device verification.
