# Actual Auto Move and Stop command V399–V402

Registered V388 is unchanged, SHA-256
`1629f2823aa953507c0ec3029556701509fd28d364824aefb6ce2aa61109abcc`.
No ROM, artwork, save progress or live RAM was edited. The original normally
created Riga battery checkpoint remains byte-exact.

## Normal route and arrival

V399 cold-boots the genuine Riga save created in V396 and verified by V398.
Port > Depart gives crew/fatigue cautions and an endurance estimate, then opens
Sail / Auto Move / Deck View. Selecting Auto Move, Stockholm on the actual map
and confirming starts automatic travel. It reaches Dock at Stockholm? and
ordinary A opens the Stockholm town. No route/unlock/eligibility flag is patched.

This establishes a successful current ordinary route, replacing earlier failed
Hamburg requests as the relevant Stop-command acquisition path. The two Riga
departure cautions are warnings; they do not block this observed Auto Move.
No Inn rest or crew adjustment was committed in this run.

## Complete actual footer and confirmed stop

V400 replays the same inputs with every frame7200..7600 captured. Frame7300 is
active automatic sailing. Independent native font masks match all323 glyph
pixels and every blank cell in these complete labels:

| Label | Native bounds | Glyph pixels |
| --- | --- | --- |
| Menu | 59,370 to83,381 | 68 |
| Inspect | 105,370 to147,381 | 80 |
| Stop Auto Move | 169,370 to253,381 | 175 |

The full Stop label fits within256 pixels; neither initial S nor final e is lost.
The small search rectangle initially used for Menu excluded its final glyph;
the complete bounds above are verified without changing the image or ROM.

V401 adds only ordinary B at7301. The complete Stop automatic movement? question
matches286 native glyph pixels, including punctuation. V402 additionally presses
A at7361 to confirm. All61 whole frames7300..7360 match V401 exactly, and sampled
frames before B match V400. At7600, complete Rotate, Menu, Inspect and Sails
captions replace the automatic footer, proving the observed return to manual
sailing. The original getter02082C4C on the final read-only RAM export returns
the cleared automatic flag. Pre-stop native flag RAM was not exported and is
not credited as an independent before/after flag comparison.

The actual Auto Move popup, Dock at Stockholm? prompt and final Stockholm town
header also pass complete native font masks. All401 dense trip captures, other
captures, input schedules, ROM/manifest and donor hashes are verified.

Verifier: `scripts/verify_auto_move_actual_v402.py`; targeted Ruff passes.
Proof: `work/analysis/auto_move_riga_v399/actual_auto_move_proof.json`.
Actual reports: `work/emulation_v193/auto_move_riga_v399/`,
`auto_move_dense_v400/`, `auto_move_stop_v401/`, `auto_move_stop_confirm_v402/`.
Finalized guide screenshot:
`E:\Rota Nova translations\Screenshots\auto-move-stop-command-v388.png`.

## Audit disposition and remaining scope

The particular actual Stop Auto Move display/input gate recorded in V318 is now
verified on current V388. This is not coverage of every automatic route, speed
mode, weather/condition, transition or hardware device. Occupied Weapon/Armor,
further health/mood states, original raw graphics consumers and deeper Gallery/
ending/regional contexts remain open. All18 plaque/hint entries remain
fully_completed:false; all22 historical requirements remain in the ledger.
The graphics goal remains active and incomplete. Low-resolution Online images
remain user-exempt. Revisit older record-based checks at full goal completion.
