# V462 normal recovery and prepared officer checkpoint

Previous goal turn: progress on linked navigation Help. This turn prepares a
genuine saved fleet for the occupied Weapon/Armor graphics gate. V461 is unchanged;
no new ROM, item, unlock, live RAM or statistic edits are made.

## Recovery and officer assignments

An isolated copy of the normal Copenhagen save loads through the game's sixth
slot. The Port Worker warns that sailors are tired; the displayed fatigue is36.
The Inn's ordinary Stay More→30 nights confirmation advances the observed date
from May17 to June16 and lowers displayed fatigue to0. Coins/date are visual
observations, not independently verified economy/calendar arithmetic. Complete
fatigue masks and literal confirmation words are checked; the substituted number
and custom date font are not credited as independent numeric-glyph proofs.

Normal Deck→Crew→Explore places Charles at the Helm and officers on masts, leaving
Survey/Galley unstaffed. Ordinary assignment controls select an officer, press A,
choose the destination and press A again. Gerhard moves from a mast to Galley;
Manuel moves from the other mast to Survey. Hodram remains Captain and Charles
remains at the Helm. The available party has no eligible Surgeon at Observe150.
No successful long voyage, armor acquisition or fatigue-rate calculation is claimed.

## Normal save and reload

The normal Save menu confirms overwriting the isolated sixth slot. The replay then
runs3800 frames after confirmation, visibly returning to Functions before stopping.
The completed battery is copied byte exactly to a new test donor and cold-loaded.
June16, zero fatigue and all four assignments survive the normal load. Original
Blue Oak clue getter4A394 still returns1. The original donor on E is hash exact.

All four reloaded room/name captions have complete native masks: Galley/Gerhard,
Survey/Manuel, Helm/Charles and Captain/Hodram. The screenshots are actual DeSmuME
framebuffer captures, not constructed views. This is targeted emulator testing,
not a complete playthrough, hardware test or proof of every room's effects.

Verifier: `scripts/verify_crew_preparation_v462.py` (targeted Ruff passes).
Proof: `work/analysis/crew_preparation_v462/preparation_proof.json`.
Actual reports: `work/emulation_v193/crew_preparation_v462/capture_report.json`
and `work/emulation_v193/crew_preparation_reload_v462/capture_report.json`.

## Saved checkpoint and next work

`E:\Rota Nova translations\Saves\hodram-copenhagen-rested-prepared-v461.dsv`

SHA-256: `ea9265b93e599fcd7c95abe20ce8e68372cfe5d6355fe7b67d2fa1592dc37e73`

Two final Deck captures are saved to E Screenshots. V461's ROM/patch remains the
one documented in `navigation_help_v461_checkpoint.md`.

Actual screens expose terminology requiring reconciliation: Deck uses Vigor and
Speech; Sailor Info uses Vigor, Sword and Talk, while some recent Help uses
Health, Combat and Social. These are recorded as audit findings, not silently
marked consistent. Review exact source/runtime dictionaries before correction.

Continue the armor voyage from this prepared checkpoint using a corrected course
and regular resupply. All22 historical requirements and all18 plaque entries
remain incomplete where open; neither Weapon nor Armor is acquired/equipped.
The full graphics goal remains active. Revisit older record-based checks at true
full-goal completion.


### V464 observation correction

Complete native glyph masks prove the full Swords and Speech labels,not Sword/Talk.
Vigor/Guile are also complete and match the active ten-entry runtime dictionary.
The ambiguity was a tiny-image reading error. Only Help terminology needed correction.
See skill_terms_v464_checkpoint.md and UI_term_proof.json.
