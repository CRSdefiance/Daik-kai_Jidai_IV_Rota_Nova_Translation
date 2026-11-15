# V701: six exact control graphics in the original live widget

## Result and scope

The previous goal turn made progress through V700's bounded Thumb search and
source-bound diagnosis of the first V698 standalone replay failure. This checkpoint
adds actual emulator loading/display evidence for Confirm,Pick Cargo,Pick Ship,
Done,Rank and Cancel. It does not discover their normal parent screens.

Seven complete7,000-frame cold boots use the unchanged V692 ROM, the existing V476
prepared Syracuse equipment donor and normal navigation to Sailor Info. Six use
an explicitly declared diagnostic widget fixture; one keeps the original screen.
The original character remains Hodram throughout; no actor,inventory,story flag,
location or quest state changes.

The original `22CPersonInformationView` contains a live type4 image widget at
021901C0. At its first ordinary wrapper call atframe5923, the fixture changes
only six source-view words: resource owner,source X/Y,palette selector,width,height.
Each normal paint then receives a temporary ARM9 R3 argument pointing to an
unchanged registered coordinate pair `(192,64)` at0213BEE4. Neither that pair nor
the original `(84,76)` pair is edited. Source files,source palettes,code and source
pixels are never injected or replaced.

|Control|Exact ROM file/source XYWH|Fixture palette bank|
|---|---|---:|
|Confirm|`/_pxl/kakutei.pxl`,0,0,48,20|0|
|Pick Cargo|`/_pxl/__frame.pxl`,208,32,48,8|9|
|Pick Ship|same,208,40,32,8|9|
|Done|same,240,40,16,8|9|
|Rank|same,184,48,24,8|9|
|Cancel|same,208,48,48,8|9|

These palette/placement inputs are explicit diagnostic choices, not evidence of
the intended ordinary control palettes or parent geometry. The gender glyph is
temporarily replaced by the fixture; this is not a production screen redesign.

## Actual loading and source binding

Confirm's original resource owner begins uncached (indexFFFFFFFF). The actual
original SDK Open call requests `_pxl/kakutei.pxl` atframe5923. The original loader
populates its cache and the original copy receives the entire exact532-byte file.
No SDK bridge or file substitution is used. The original Frame resource is already
available through ordinary UI use.

The actual first copy arguments bind complete source files,source rectangles,
palette bank and destination. Fourteen complete original cache-getter calls from
the two held snapshots per run return exact current ROM files,with full saved-
register/stack ABI and no SDK I/O bridge. Every executed getter instruction matches
the clean original. This verifies these actual source bindings without claiming
full arbitrary parent-update or I/O-model equivalence.

## Pixel and restoration checks

- Both held frames6200/6400 verify all six complete control rectangles:12 crops,
  **4,608 native five-bit pixels**, including all blank,leading and trailing cells.
- All12 complete two-screen images (1,179,648 native five-bit pixels) match a source-
  derived model. The original Person Info background predicts the removed gender
  view, and actual source palette words predict the temporary control. Whole RGB
  differences from the baseline occur at exactly the independently predicted
  changed pixels; no other display difference is waived.
- The stored palette alpha bit governs the tested source path. Confirm's index14
  is transparent while index0 is opaque. The initially considered index0-only
  transparency model is rejected. This is a corrected expected-pixel model,
  not a ROM palette/alpha change.
- Twelve negative controls reject one-pixel placement errors and either the
  wrong Frame palette or Confirm's wrong index0 transparency assumption.
- All90 pre-fixture whole RGB/4 MiB RAM pairs match. All six pre-write complete
  RAM states,initial widget CPU128 states and original view words match.
- Each install/restore proves all main-RAM bytes exact except the six declared
  source words,and leaves CPU/DTCM/ITCM unchanged. Every CPU argument redirect
  changes only R3. Its host interval is disjoint from the RAM/TCM buffers.
- All source words are restored atframe6401. At6500 the live widget is exact to
  its original inputs; after B6501 its parent is destroyed,so freed/reused heap
  bytes are not treated as live persistent fields. All18 complete restored Info/
  roster RGB pairs at6500/6600/7000 match the normal baseline exactly.
- Fifteen native host-prefix/ABI,eight bounded-read and four wrong-call-argument
  controls pass. All host slots are restored and the core file is unchanged.

The verifier's initial assertion that restored view fields must also persist
after the parent was destroyed was rejected. Its diagnostic showed6500 exact and
6600/7000 reused heap bytes. The final check verifies live inputs before destruction
and complete restored display afterward. No game change was inferred from that
test-lifetime mistake.

## Visual review and remaining gates

Both the six complete fixture-screen sheet and the original/restored Info/roster
sheet were opened. All labels are complete and readable at their native compact
sizes; Confirm's border and padding remain intact. The restored portrait,gender,
zodiac,item selection and roster return show the original character correctly.
These diagnostic layouts are not normal gameplay screenshots or guide candidates.

This closes fixture-based original loader/widget/crop coverage for these six
graphics. Normal control locations,intended palettes/selection states,embedded
copy use and ordinary interactions remain unverified. It is not a global unused-
resource claim and does not clear V698's native-prefix or V694's suffix-model gaps.

All18 original plaque/hint entries remain incomplete and all22 historical scope
objects remain exact. Comic playback,remaining legacy/embedded contexts,texture/
restoration review,older record checks and final acceptance remain open. The full
graphics goal stays active.

## Release and evidence

V692 ROM SHA256 remains
`0ff197ce9bbb48898c74a3c664609196867a5662bc3b346c612709038c54a47e`.
No artwork,ROM,patch,manifest,registry,donor,canonical baseline or release pointer
changes; no new ROM,commit or push.

- Analysis: `work/analysis/small_controls_v701/`.
- Captures: `E:/Rota Nova translations/Generated/work/emulation_v193/small_controls_v701_*`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V701 Small control widget displays`.
- Runner/verifier: `scripts/run_small_controls_v701.py`, `scripts/verify_small_controls_v701.py`.
