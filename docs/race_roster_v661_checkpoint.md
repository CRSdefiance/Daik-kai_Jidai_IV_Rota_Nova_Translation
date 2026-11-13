# V661: Grand Race roster cards and separate ready footer

## Result and limits

V653 completes three targeted cold boots: a 4,400-frame lone-host baseline and
two 5,000-frame runs with explicitly isolated UI fixtures. The original controller
displays four participant cards after a receive-ring fixture. A separate
readiness-only fixture displays the original Back / Select footer. This is not
wireless multiplayer, an earned unlock, a completed race, or simultaneous proof
of four participants and a ready footer. WiFi emulation is off.

The previous status-only answer was no progress toward the goal. This continuation
revalidated the current files, completed the tests below and adds evidence. The
complete graphics objective remains active.

## Source conditions and retained unsuccessful attempts

Actual host controller is `020F98FC`, with CNetMenu root `021929B4` and four
76-byte card objects starting `02192820`. These legacy objects call the function
at vtable offset zero; the generic scene-node draw offset does not apply.

Original `020FB528` publishes the local packet and calls SDK accessor `0210C524`.
That accessor checks both membership/valid masks and computes a 52-byte stride
through `0210C4E8`. `020FA5B0` copies character, ship class, 17-byte captain field
and 19-byte ship field into the controller. `020FAD38` sets the original portrait
view, and `020FABB0` paints each complete card.

The first fixture wrote output packets at `0237B640`. Original `0210CB74` promptly
replaced these from the receive ring, leaving only the local participant. The
separate ready halfword at `0237D9F0` still exercised the footer condition. These
events, captures and the original runner are retained; this attempt gets no
four-card credit.

The successful fixture writes only the first 212 bytes of each original 512-byte
ring slot at `0237BBC0 + slot*512`, plus the declared readiness halfword. Original
`0210CD3C..0210CD74` consumes the records normally. Original ring counters are not
patched. Four rendered cards contain Maria / Chun, Rafael / Test Ship 2, Hodram /
Test Ship 3 and Lil / Test Ship 4. The three Test Ship names are fixture labels.
Chun is the donor's persisted ship name, not a new default character spelling.

The original recipient packet fixture is restored at frame4601. Both test runs
return to a whole-screen-exact copy of their initial lone-host waiting state at
frame4690. B returns normally before frame5000. Original donor save, all ROMs,
patch, manifest and registry hashes remain unchanged.

## Complete card checks

- Four frames contain 32 complete captain/ship fields, including every leading
  and trailing letter; all64 first/final deletion controls are rejected.
- The source-defined portrait rectangles are 64x72. Text rectangles are 116x34;
  the right-hand cards start at x72, while left-hand cards start at x68.
- Native packet access, copy, view setup and painting execute for all four cards.
  All34,208 card pixels are reconstructed over poison. No old card output is read
  before it is written, all other lower-buffer bytes stay exact, and all49,152
  resulting lower RGB pixels match the capture.
- Every executed instruction matches the registered ARM9/overlay and Japanese
  source. The actual captured portrait cache supplies the native portrait inputs;
  this checkpoint does not claim a new independent ROM portrait-art transcript.
- An early replay from a lone-host capture failed because other portrait state
  was not initialized. A uniform text-box origin assumption also failed. Both are
  retained; the final replay uses the actual four-card state and original geometry.
- Four pre-fixture whole frames match across all three cold boots. Four-card
  samples remain identical across both nominal ready phases: this run does not
  establish an active ready footer with four actual wireless participants.

## Which Confirm is this?

Original `020FB6A0` supplies the readiness halfword. Original host branch
`020F9E94..020F9EBC` selects descriptor `0211B620` (Back) or `0211B650` (Back and
Select), then calls `020CA890`. The latter descriptor points to literal `Select`
at `0211B51C`; it uses the existing footer text measurement/drawing path.

The ready-only fixture changes exactly1,228 captured pixels, confined to
`[154,368,251,384)`. Clearing it restores the whole prior screen. The four existing
English footer measure/draw/gap adaptation words are explicitly accounted for by
`help_footer_release_v3`, rather than falsely called byte-identical Japanese code.

This resolves this particular Grand Race waiting-room lead as a text footer.
It does not establish an actual consumer for `/_pxl/kakutei.pxl`, Done, Rank,
Cancel, Pick Cargo or Pick Ship. All six parent requirements remain open. No
native full-footer lettering or full-scene source reconstruction is claimed here.

## Evidence and unchanged goal

- Verify: `python scripts/verify_race_roster_v661.py`.
- Proof: `work/analysis/race_roster_v661/proof.json`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V661 Grand Race roster`.
- All screenshots remain labeled testing fixtures; none is promoted for a guide.
- ROM stays `out/all_routes_combined_v653_candidate.nds`, SHA256
  `c4e9c4faf18c212e5b6572d61e6b2821493f38bbc1dc89d601b37b16058b3ade`.

All18 original plaque/hint entries remain incomplete and all22 historical scope
objects remain exact. Other control/card/legacy/material/equipment/gameplay and
final acceptance requirements remain open. The low-resolution Online exclusions,
preserved brown marks and older record-check obligation remain in force. No ROM
build, canonical promotion, commit or push occurs in this checkpoint.
