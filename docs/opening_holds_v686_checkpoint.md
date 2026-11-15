# V686: three Maria pauses are original script waits

## Result

Three empty lower-screen holds in Maria's opening are explicit original script
waits, not English padding pages. The original Japanese ROM and V685 both execute
opcode `2000` at chapter 33 offsets 32, 120 and 1708. Each calls original
`02054E44(0,0)` from `0202A214`, returning to `0202A218`.

Read-only tracing observes the real entry and return around all six selected
source/current captures. No native return, GUI completion, game RAM, story state
or screenshot is substituted in these live runs. Every callback preserves the
CPU prefix, full main RAM, DTCM and configuration; both host slots restore.
There are 99 callbacks: 12 selected events and 87 other modal callers.

| Original frame | V685 frame | Chapter offset | Original return | V685 return |
|---|---|---|---|---|
| 4000 | 4000 | 32 | 4016 | 4015 |
| 5800 | 5800 | 120 | 5815 | 5817 |
| 22000 | 21400 | 1708 | 22015 | 21416 |

All returns follow the first subsequent A press and precede the next scheduled
action. The return is 14–16 frames after A begins, after the eight-frame press
has ended. The initial verifier incorrectly required return during those eight
frames. Its code and failure log remain retained. No particular nested cleanup
or timing mechanism is inferred from the corrected measurement.

## Source and visual controls

The complete native dispatch was also replayed for six source/current cases,
with only GUI modal completion bridged. That isolated component check is distinct
from the unbridged actual entry/return traces. Five non-wait continuation controls
bind actual VM positions, complete resident chapter bytes and original commands.
Ten native prefix and eight memory-mirror controls pass.

The source/current screenshots must be matched by script position. Comparing
both versions at frame 21400 compares different commands: the source's preceding
Japanese paragraph remains active for one additional sampled input step. This
is not a general screenshot lag adjustment.

All three whole upper screens match, and all six complete lower dialogue regions
contain no source-palette text pixels. Two whole paper rectangles match. At 5800,
208 RGB differences remain within the 16×16 A indicator. They are disclosed,
not masked or counted as whole-region equivalence. Its native paint/phase is
not independently established by this checkpoint.

The corrected script-position comparison sheet was opened and reviewed. The
third source continuation column is explicitly a later crew-join control, not
the immediately following translated sentence. The original run ends at that
join; it does not receive full opening-to-town credit.

Two observed 31000-frame cold boots match 24 complete two-screen baseline pairs
and two complete terminal RAM states. The separate original source control is
also terminal. All use the same 53 normal controller actions and the existing,
byte-exact authorized system-unlock donor copied before boot. No savestate or
live location/inventory/movie fixture is used. Unlock access is not earned-game
evidence. Retained V685 Maria opening and baseline runs supply current controls.

## Scope and storage

Only these three specific blank holds are closed as original waits. This does
not clear every blank page, older dialogue wording, all route graphics, hardware
behavior or final acceptance. All 18 plaque/hint objects remain incomplete and
all 22 historical requirements remain exact. The preceding status-only turn was
no progress; this checkpoint completes and records evidence.

V685 remains the latest compiled experimental candidate:
`out/all_routes_combined_v685_candidate.nds`, SHA256
`83e7bdc7c4926ad69eb04704e8327aba50d0fe29b00cce7f5f59d4be8c203150`.
ROM, patch, registry, canonical baseline and all release pointers are unchanged.

- Analysis: `work/analysis/opening_holds_v686`.
- Proofs: `proof.json` and `actual_wait_proof.json`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V686 Original scene waits`.
- No guide promotion, new ROM, commit or push.
