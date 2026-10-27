# Shared text regression and V152 alignment repair

Broad translation work is paused at the user's request. The current task is
repairing the severe runtime text regressions documented in six V151 screenshots.
After the V152 handoff the user confirms all six cases are corrected. A separate
unreadable Ceuta tutorial exposes an older system-selector conversion. V152 is
now revoked as a playable candidate; experimental V153 retains this entire copy
repair and fixes all 13 affected tutorial panels. See
`raphael_system_panel_regression_v153.md` for current artifacts and coverage.
The user also confirms V92 works, V120 fails, and Lil's route fails in the exact
`all_routes_combined_v105_candidate.nds` build. This is not release acceptance.

## Reproduced cause

The native shared copy helper at `020CEC74` chooses word/halfword/byte copying
from the byte count alone. It never checks source or destination alignment.
COMMON repacking changes the offsets of unrelated packed neighbors, exposing
unaligned pointers to this helper. ARM946 word loads align down and rotate the
loaded word; unaligned stores align down. The ordinary Unicorn fixtures did not
model this behavior and therefore reported byte-preserving copies incorrectly.

Executing the actual native COMMON lookup/copy with explicit ARM946 load behavior
reproduces the screenshot strings:

| Message | Expected | Broken V151 output |
| --- | --- | --- |
| 8 | Need help? | `Ne   hedp?el` |
| 50 | Welcome. Please, come inside. | `W` |
| 51 | Welcome! What will you have? | `W ` |
| 53 | 5 coins. | `5ns.i co ns.` |
| 120 | Everything correct? | `Ev  yternghior cctre  ? ` |

The native renderer separately requests the correct glyphs when supplied intact
text. These five reproductions establish a fault before rendering, rather than
translation wording. Recruitment corruption uses the same shared path; actual
the user now confirms the reported recruitment cases; full Lil-route gameplay
remains unverified.

## Historical boundary

The five-message native comparison passes in every available combined build
checked from V92 through V103. V104 first fails messages 50, 51 and 53; V105 also
fails confirmation 120. V119, V120 and V151 fail all five. This establishes the
boundary for these five cases, not the earliest defect in every scene.
V104 adds `common_native_repack_v104.json` and its offset table, authored from
COMMON block 0. V105 adds block 1 repacking. This explains why unrelated old
messages break when newly translated entries change their neighboring offsets.
Evidence: `work/analysis/common_alignment_historical_build_comparison.json`.
Combined V104–V151 registry profiles are revoked; retain diagnostic artifacts.

## System repair

V152 replaces the shared helper's entry with an inline alignment guard in its
former halfword-dispatch region. The unchanged word loop is selected only when
source, destination and byte count are all divisible by four. Every other input
uses the unchanged byte loop. No text is shortened, rewritten or padded to hide
the failure. This repairs the alignment contract for every caller of this helper,
including future packed messages and names.

The transform changes only the entry word and the 44-byte guard region inside
ARM9. No additional code section, pool, heap boundary, name pointer, story record,
COMMON selection, font or graphics bytes change from V151. The staged ARM7 boot
repair remains present. Strict source/target and native-proof hashes are enforced.

## Evidence

All 3,668 saved COMMON selections pass actual native lookup/copy with modeled
ARM946 alignment, both warm and cold: **7,336 cases**. Cold filesystem open/read
remain host contracts; ILNK/cache/copy execute. A separate **704-case** native
copy matrix tests every source/destination byte phase, zero/small counts and
boundary lengths through 4,096 bytes. Full payloads, leading/final bytes, source
preservation and neighboring guards pass. The five unpatched failures above are
required to reproduce before the repaired proof can pass.

Saved V152 matches the strict transform byte for byte. Every other ROM component,
all 3,668 COMMON selections and the inherited 435-batch order are preserved.
Canonical baseline/menu checks pass; the clean-ROM patch reconstructs exactly.
Earlier copy evidence lacking ARM946 alignment cannot be used as runtime-layout
approval. Revisit those older record-based checks after this regression is resolved.

## Historical V152 handoff (now revoked; use experimental V153)

- ROM: `out/all_routes_combined_v152_candidate.nds`.
- ROM SHA-256: `2bea1a9554989e241cb57e8b398e8d5aa90855ea5f9cbef474bd34fbf1be1e63`.
- ARM9 SHA-256: `21e2be34e965fd17fc56dd18e919e411b7da87a3c8f56f9e7e6fd8c39100940b`.
- Patch: `out/all_routes_combined_v152_candidate.xdelta`, 744,113 bytes.
- Patch SHA-256: `dbd1fd202ac0cde985433e78eae47d6ca6f2ace40f2deeac52bf3945a77aa165`.
- Manifest beside ROM; profile `all-routes-unified-v152`, now revoked.
- Canonical builder base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- All accepted layers and 435 inherited batches/postprocessing stages retained.
- Changed canonical paths: `/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`,
  `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`,
  `/data/SC0.DK4`, `/data/SC1.DK4`, `/data/SC2.DK4`, `/data/SC3.DK4`.
- Verifiers: `probe_common_copy_arm946_alignment.py`,
  `verify_common_copy_alignment_v152.py`, `verify_release_baseline.py`; lint passes.

Cold-boot without a savestate. Check the New Game confirmation, both recruitment
messages, Trader greeting, Barkeep greeting and drink-price response shown in the
six screenshots, then Lil's opening transitions and town dialogue. Verify leading
characters, complete wording, portrait/name state and line breaks. Full gameplay,
hardware cache behavior and native frame/input composition remain unverified.
Do not promote without explicit user acceptance. Keep broader translation paused.
