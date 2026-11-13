# Actual Relaxed mood and plaque replay V392

This checkpoint uses the unchanged registered V388 candidate, SHA-256
`1629f2823aa953507c0ec3029556701509fd28d364824aefb6ce2aa61109abcc`.
No ROM, patch, artwork, save progress or live RAM was edited.

## Genuine display evidence

The interactive V391 cold boot loads the unchanged genuine V328 battery save
normally. A second unattended cold boot reproduces its controller/touch schedule
through the first sailing-menu opening. All 34 captured whole frames through
frame12400 are byte-identical. The replay opens all four officers before further
sailing can change their moods. No savestate or synthetic progression is used.

| Frame | Officer | Health | Mood |
| --- | --- | --- | --- |
| 14000 | Hodram Joakim Bergstrom | Healthy | Normal |
| 15200 | Gerhard Ardelknatts | Healthy | Relaxed |
| 16400 | Manuel Almeida | Healthy | Normal |
| 17600 | Charles Jean Rochefort | Healthy | Upset |

`scripts/verify_plaque_relaxed_v392.py` verifies the ROM/manifest, capture hashes,
all four complete names, eight complete condition masks, forty complete plaque
regions and forty complete skill lines. Every leading/final glyph and blank cell
within those masks is checked. The Relaxed mood is new actual GPU evidence; its
specific cause is not established. Targeted Ruff passes.

Proof: `work/analysis/plaque_relaxed_v392/display_proof.json`.
Actual report: `work/emulation_v193/plaque_relaxed_v392/capture_report.json`.
The verified Gerhard screenshot is copied without editing to
`E:\Rota Nova translations\Screenshots\sailor-info-gerhard-relaxed-v388.png`.

## Navigation evidence and limits

`scripts/read_navigation_snapshot_v391.py` runs original environment/fleet/ship
getters against read-only captured RAM in an isolated native machine. Eight
hashed samples record the packed direction byte and native world point. These
are raw fields; their compass mapping and response to long inputs are not yet
established. The samples contain no active hazard positions. They do not prove
a port arrival, tornado encounter, treasure or equipment acquisition.

The longer V391 voyage produced readable No Water and No Food warning screens.
Those warnings alone are not credited as alternate health-state verification.
The final officer displays remain Healthy. The underlying battery donor's earlier
history is unknown; only the captured/replayed session is proven here.

## Remaining requirements

All eighteen plaque/hint entries remain `fully_completed:false`. Actual occupied
Weapon/Armor, further health/mood states and broader route/fleet contexts remain.
All twenty-two historical graphics requirements remain in the completion ledger,
including outstanding original consumers, Gallery/endings and regional contexts.
Low-resolution Online images remain user-exempt. This is a targeted automated
emulator test, not a full playthrough or a physical-device test. The graphics goal
stays active. Revisit older record-based checks when the full goal is complete.
